from crawler.crawler import Crawler
import csv

import utils

config = utils.get_config()
FILE_PATH = "data.csv"

if __name__ == "__main__":
    for target in config["targets"]:
        crawler = Crawler(config=target)
        articles = crawler.crawl()
        fieldnames = articles[0].keys()
        with open(FILE_PATH, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(articles)
