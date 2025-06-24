import pandas as pd
import re
import py_vncorenlp
from sklearn.feature_extraction.text import TfidfVectorizer

with open("vietnamese-stopwords-dash.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f if line.strip())

df = pd.read_csv("data.csv")

rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir="/etc/vncorenlp")


def tokenize_and_filter(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-ZÀ-ỹà-ỹ0-9\s]", " ", text)
    segmented_sentences = rdrsegmenter.word_segment(text)
    tokens = " ".join(segmented_sentences).split()
    tokens = [t for t in tokens if t not in stopwords and len(t) > 1]
    return tokens


def process_row(row):
    combined_text = f"{row['title']} {row['summary']} {row['content']}"
    return tokenize_and_filter(combined_text)


tokenized_docs = df.fillna("").apply(process_row, axis=1)

df["tokens"] = tokenized_docs


docs_as_text = df["tokens"].apply(lambda tokens: " ".join(tokens))

vectorizer = TfidfVectorizer(
    ngram_range=(2, 3),
    max_df=0.95,
    min_df=2,
)

X = vectorizer.fit_transform(docs_as_text)

mean_scores = X.mean(axis=0).A1
vocab = vectorizer.get_feature_names_out()
top_n = 30
top_indices = mean_scores.argsort()[::-1][:top_n]
top_ngrams = [(vocab[i], mean_scores[i]) for i in top_indices]

print("Top N-grams:")
for phrase, score in top_ngrams:
    print(f"{phrase:<30} {score:.4f}")
