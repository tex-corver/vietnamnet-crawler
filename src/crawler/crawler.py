import requests
from bs4 import BeautifulSoup
import time
import random


class Crawler:
    def __init__(self):
        self.base_url = "https://vietnamnet.vn"
        self.max_pages = 10
        self.max_retries = 5
        self.initial_delay = 1

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
        response = self.request_with_backoff(self.base_url)
        if not response:
            print("Failed to fetch the webpage after retries.")
            exit()

        soup = BeautifulSoup(response.text, "html.parser")
        category_items = soup.find_all("li", class_="mainNav__list-item swiper-slide")
        categories = [
            item.get("routeractive")
            for item in category_items
            if item.get("routeractive")
        ]
        return categories

    def fetch_articles(self, category):
        url = self.base_url + category
        links = []
        for page in range(0, self.max_pages):
            page_url = url + f"-page{page}/"
            response = self.request_with_backoff(page_url)
            if not response:
                print(f"Failed to fetch page {page_url} after retries.")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all(
                "h3", class_="horizontalPost__main-title vnn-title title-bold"
            )
            for article in articles:
                link = article.find("a")
                if link:
                    links.append(link.get("href"))
        return links

    def fetch_article(self, link):
        if self.base_url not in link:
            url = self.base_url + link
        else:
            url = link

        print(f"Fetching article: {url}")

        response = self.request_with_backoff(url)
        if not response:
            print(f"Failed to fetch article {url} after retries.")
            return {}

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", class_="content-detail-title")
        title = title.text.strip() if title else "N/A"

        author = soup.find("p", class_="article-detail-author__info")
        author = " ".join(author.text.split()) if author else "N/A"

        summary = soup.find("h2", class_="content-detail-sapo sm-sapo-mb-0")
        summary = summary.text.strip() if summary else "N/A"

        content = soup.find("div", class_="maincontent main-content")
        content = " ".join(content.text.split()) if content else "N/A"

        time = soup.find("div", class_="bread-crumb-detail__time")
        time = time.text.strip() if time else "N/A"

        return {
            "url": url,
            "title": title,
            "author": author,
            "time": time,
            "summary": summary,
            "content": content,
        }

    def request_with_backoff(self, url):
        delay = self.initial_delay
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request failed ({url}): {e}")
                if attempt == self.max_retries - 1:
                    print("Max retries reached. Skipping...")
                    return None
                wait_time = delay + random.uniform(0, 1)
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                delay *= 2
        return None
