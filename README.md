# vietnamnet-crawler

# Getting started

## Installation

-   Clone the repository
-   Set up configuration

    You can store the information of the targets in .configs/targets.yaml

    Example targets.yaml:
    
    ```yaml
    targets:
    - base_url: https://vietnamnet.vn
        initial_delay: 1              # Delay in seconds before first request
        max_retries: 5                # Retry attempts if request fails
        max_pages: 1                  # Number of paginated pages to crawl
        page_prefix: -page            # URL pattern for pagination
        category:
          tag: li                                      # HTML tag to find category links
          class: mainNav__list-item swiper-slide       # Class used to identify category elements in the menu
        article:
          tag: h3                                      # HTML tag that wraps article links on the category page
          class: horizontalPost__main-title vnn-title title-bold  # Class identifying article titles or links
        title:
          - [h1, content-detail-title]                 # List of possible [tag, class] pairs used to locate the article title
        author:
          - [p, article-detail-author__info]           # List of possible [tag, class] used to locate the author's name on the article page
        summary:
          - [h2, content-detail-sapo sm-sapo-mb-0]     # List of possible [tag, class] used to extract the article summary
        content:
          - [div, maincontent main-content]            # List of possible [tag, class] that contains the full article content
        time:
          - [div, bread-crumb-detail__time]            # List of possible [tag, class] to extract the publishing time of the article
    ```

    **You can add multiple targets (websites) under the targets: list to crawl more than one news source.**
    
## Development requirements

This repository uses `poetry 1.8.5` (as shown by the poetry.lock file).


-   Install `poetry 1.8.5` if you haven't already:

    ```
    pip install poetry==1.8.5
    ```

-   Installing dependencies:

    ```
    poetry install
    ```

# Running the Script

-   To run the tests, simply use the make command:

    ```bash
    make local-run
    ```

# Sample Output

-   Data is saved to the `data.csv` file. Here's an example of what one row looks like in the CSV:

    ```csv
    category,url,title,author,summary,content,time
    /chinh-tri,https://vietnamnet.vn/dieu-ngo-ngang-tu-ket-luan-thanh-tra-du-an-benh-vien-bach-mai-viet-duc-co-so-2-2388202.html,"Điều ngỡ ngàng từ kết luận thanh tra dự án bệnh viện Bạch Mai, Việt Đức cơ sở 2", "TS Đinh Văn Minh", "Kết quả thanh tra dự án đầu tư xây dựng cơ sở 2 của bệnh viện Bạch Mai và bệnh viện Việt Đức vừa được công bố khiến mọi người phải ngỡ ngàng.", "Không phải là những thiệt hại khủng khiếp đã gây ra trong quá trình triển khai thực hiện dự án, mà chính cái cách để xảy ra sai phạm mới là điều khiến cho không ít người bất ngờ ...", "Chủ Nhật, 06/04/2025 - 17:07"
    ```
    
-   Each article row includes:

    `category` – the news section

    `url` – direct link to the article
    
    `title` – the headline
    
    `author` – journalist name
    
    `summary` – subheading
    
    `content` – full article body
    
    `time` – publication date/time
