import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.base_url = "https://vietnamnet.vn"
        self.max_pages = 10

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
        response = requests.get(self.base_url)
        if response.status_code == 200:
            html = response.text
        else:
            print("Failed to fetch the webpage:", response.status_code)
            exit()

        soup = BeautifulSoup(html, "html.parser")

        category_items = soup.find_all("li", class_="mainNav__list-item swiper-slide")

        categories = []
        for item in category_items:
            path = item.get("routeractive")
            if path:
                categories.append(path)

        return categories

    def fetch_articles(self, category):
        url = self.base_url + category
        links = []
        for page in range(0, self.max_pages):
            page_url = url + f"-page{page}/"

            response = requests.get(page_url)
            if response.status_code == 200:
                html = response.text
            else:
                print("Failed to fetch the webpage:", response.status_code)
                exit()

            soup = BeautifulSoup(html, "html.parser")

            articles = soup.find_all(
                "h3", class_="horizontalPost__main-title vnn-title title-bold"
            )
            for article in articles:
                link = article.find("a")
                links.append(link.get("href"))

        return links

    def fetch_article(self, link):
        url = self.base_url + link
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch article {url}: {e}")
            return {}

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("h1", class_="content-detail-title")
        if title:
            title = title.text
        else:
            title = "N/A"

        author = soup.find("p", class_="article-detail-author__info")
        if author:
            author = author.text.replace("\n", "").replace("\r", "").strip()
            author = " ".join(author.split())
        else:
            author = "N/A"

        summary = soup.find("h2", class_="content-detail-sapo sm-sapo-mb-0")
        if summary:
            summary = summary.text
        else:
            summary = "N/A"

        content = soup.find("div", class_="maincontent main-content")
        if content:
            content = content.text.replace("\n", "").replace("\r", "").strip()
            content = " ".join(content.split())
        else:
            content = "N/A"

        time = soup.find("div", class_="bread-crumb-detail__time")
        if time:
            time = time.text.replace("\n", "").replace("\r", "").strip()
        else:
            time = "N/A"

        return {
            "url": url,
            "title": title,
            "author": author,
            "time": time,
            "summary": summary,
            "content": content,
        }
