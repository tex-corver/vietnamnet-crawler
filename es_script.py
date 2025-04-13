import pandas as pd
import elasticsearch

import utils

config = utils.get_config()["application"]
CSV_FILE = "data.csv"
INDEX_NAME = "articles"

es = elasticsearch.Elasticsearch(config["elasticsearch"]["host"])


INDEX_MAPPING = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
    },
    "mappings": {
        "properties": {
            "category": {"type": "text"},
            "url": {"type": "keyword"},
            "title": {"type": "text"},
            "author": {"type": "text"},
            "time": {"type": "text"},
            "summary": {"type": "text"},
            "content": {"type": "text"},
        }
    },
}


def create_index_if_missing():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=INDEX_MAPPING)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


def index_articles_from_csv(filepath):
    df = pd.read_csv(filepath)
    for _, row in df.iterrows():
        doc_id = str(row.get("url", ""))

        doc = {
            "category": str(row.get("category", "")),
            "url": doc_id,
            "title": str(row.get("title", "")),
            "author": str(row.get("author", "")),
            "time": str(row.get("time", "")),
            "summary": str(row.get("summary", "")),
            "content": str(row.get("content", "")),
        }

        if not es.exists(index=INDEX_NAME, id=doc_id):
            es.index(index=INDEX_NAME, id=doc_id, document=doc)
            print(f"Indexed: {doc_id}")
        else:
            print(f"Skipped (already exists): {doc_id}")


def search_articles(query, field="title"):
    body = {
        "query": {
            "match": {
                field: {
                    "query": query,
                    "operator": "and",
                }
            },
        },
    }
    result = es.search(index=INDEX_NAME, body=body)
    return [hit["_source"] for hit in result["hits"]["hits"]]


if __name__ == "__main__":
    create_index_if_missing()
    index_articles_from_csv(CSV_FILE)

    print("\nSearch the articles:")
    field = input("Search field (title, author, time, summary, content): ")
    query = input("Search query: ")

    hits = search_articles(query, field)
    print(f"\nFound {len(hits)} result(s):\n")
    for article in hits:
        print(f"- {article['title']} ({article['url']})")
