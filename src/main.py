from crawler.crawler import Crawler
import csv

if __name__ == "__main__":
    crawler = Crawler()
    articles = crawler.crawl()
    file_path = "data.csv"
    fieldnames = articles[0].keys()
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(articles)
