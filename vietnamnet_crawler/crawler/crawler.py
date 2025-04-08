from typing import Any
import requests
import time
import random

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, config: dict[str, Any]):
        self.config = config

    def crawl(self):
        categories = self.fetch_categories()
        articles = []

        for category in categories:
            article_links = self.fetch_articles(category)
            for article_link in article_links:
                article = self.fetch_article(article_link)
                if article:
                    articles.append({"category": category} | article)
        return articles

    def fetch_categories(self):
        response = self.request_with_backoff(self.config["base_url"])
        if not response:
            print("Failed to fetch the webpage after retries.")
            exit()

        soup = BeautifulSoup(response.text, "html.parser")

        category_items = soup.find_all(
            self.config["category"]["tag"],
            class_=self.config["category"]["class"],
        )
        categories = [
            item.get("routeractive")
            for item in category_items
            if item.get("routeractive")
        ]
        return categories

    def fetch_articles(self, category):
        url = self.config["base_url"] + category
        links = []
        for page in range(0, self.config["max_pages"]):
            page_url = url + f"{self.config['page_prefix']}{page}"
            response = self.request_with_backoff(page_url)
            if not response:
                print(f"Failed to fetch page {page_url} after retries.")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all(
                self.config["article"]["tag"],
                class_=self.config["article"]["class"],
            )
            for article in articles:
                link = article.find("a")
                if link:
                    links.append(link.get("href"))
        return links

    def fetch_article(self, link):
        if self.config["base_url"] not in link:
            url = self.config["base_url"] + link
        else:
            url = link

        print(f"Fetching article: {url}")

        response = self.request_with_backoff(url)
        if not response:
            print(f"Failed to fetch article {url} after retries.")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")

        elements = [
            "title",
            "author",
            "summary",
            "content",
            "time",
        ]

        article = {}
        article["url"] = url

        for element in elements:
            for tag, class_ in self.config[element]:
                article[element] = soup.find(
                    tag,
                    class_=class_,
                )
                if article[element]:
                    article[element] = article[element].text.strip()
                    break

            if element not in article:
                article[element] = "N/A"

        return article

    def request_with_backoff(self, url: str):
        delay = self.config["initial_delay"]
        for attempt in range(self.config["max_retries"]):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request failed ({url}): {e}")
                if attempt == self.config["max_retries"] - 1:
                    print("Max retries reached. Skipping...")
                    return None
                wait_time = delay + random.uniform(0, 1)
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                delay *= 2
        return None
