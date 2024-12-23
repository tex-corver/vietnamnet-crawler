import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.base_url = "https://vietnamnet.vn/"

    def crawl(self):
        categories = self.fetch_categories()
        articles = {}
        for category in categories:
            articles[category] = self.fetch_articles(category)
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
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
        else:
            print("Failed to fetch the webpage:", response.status_code)
            exit()

        soup = BeautifulSoup(html, "html.parser")

        articles = soup.find_all(
            "h3", class_="verticalPost__main-title vnn-title title-bold"
        ) + soup.find_all(
            "h3", class_="horizontalPost__main-title vnn-title title-bold"
        )
        titles = []
        for article in articles:
            link = article.find("a")  # Find the <a> tag inside the <h3>
            if link and "title" in link.attrs:  # Check if the 'title' attribute exists
                titles.append(link["title"])  # Extract the title attribute

        return titles
