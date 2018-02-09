

class Config:
    base_url = "https://www.zhihu.com"
    url_search = "https://www.zhihu.com/search?type=content&q="

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) "
                      "CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
        "Referer": "https://www.zhihu.com/search?type=content&q="
    }

    movie_search_url = "http://www.btbtdy.com/search/{}.html"
    movie_base_url = "http://www.btbtdy.com"
    movie_download_url = "http://www.btbtdy.com/vidlist/{}.html"
