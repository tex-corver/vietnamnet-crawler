from crawler.crawler import Crawler

if __name__ == "__main__":
    crawler = Crawler()
    data = crawler.crawl()

    # Write the data to a file
    with open("output.txt", "w") as file:
        for category, articles in data.items():
            file.write(f"{category}:\n")
            for article in articles:
                file.write(f"- {article}\n")
            file.write("\n")
