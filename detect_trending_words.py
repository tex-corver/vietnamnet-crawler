import pandas as pd
import re
import py_vncorenlp

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

print(df["tokens"].iloc[0])
