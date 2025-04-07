import pandas as pd
import opensearchpy
import requests_aws4auth
import boto3

import utils

config = utils.get_config()
CSV_FILE = "data.csv"
INDEX = "articles"

session = boto3.Session()
credentials = session.get_credentials()
awsauth = requests_aws4auth.AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    config["aws"]["region"],
    "es",
    session_token=credentials.token,
)

client = opensearchpy.OpenSearch(
    **config["opensearch"],
    http_auth=awsauth,
    connection_class=opensearchpy.RequestsHttpConnection,
)


def create_index(index, body):
    if not client.indices.exists(index=index):
        client.indices.create(index=index, body=body)


def index_csv(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        doc = {
            "category": str(row["category"]),
            "url": str(row["url"]),
            "title": str(row["title"]),
            "author": str(row["author"]),
            "time": str(row["time"]),
            "summary": str(row["summary"]),
            "content": str(row["content"]),
        }
        doc_id = row["url"]
        exist = client.exists(index=INDEX, id=doc_id)
        if exist:
            continue
        r = client.index(index=INDEX, id=doc_id, body=doc)
        print("Indexed", r["_id"])


def search(query, field="title"):
    body = {
        "query": {
            "match": {
                field: query,
            },
        },
    }
    r = client.search(index=INDEX, body=body)
    return [hit["_source"] for hit in r["hits"]["hits"]]


if __name__ == "__main__":
    create_index(
        INDEX,
        {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 2,
            },
            "mappings": {
                "properties": {
                    "category": {
                        "type": "text",
                    },
                    "url": {
                        "type": "text",
                    },
                    "title": {
                        "type": "text",
                    },
                    "author": {
                        "type": "text",
                    },
                    "time": {
                        "type": "text",
                    },
                    "summary": {
                        "type": "text",
                    },
                    "content": {
                        "type": "text",
                    },
                },
            },
        },
    )
    index_csv(CSV_FILE)

    field = input("Search field (title, author, time, summary, content): ")
    query = input("Search query: ")

    results = search(query, field)
    for result in results:
        print(result)
