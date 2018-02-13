import re
import logging
from bs4 import BeautifulSoup
from zhihu.config import Config


def deal_zhihu_content(content):
    """
    :param content: html file
    :return: return a dict {title: url}
    """
    res = []
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all(attrs={"class": "item clearfix", "data-type": "Answer"}):
        title, url, vote = None, None, None
        for i in link.find(attrs={"class": "title"}):
            title = i.text
        for i in link.find(attrs={"class": "entry answer"}):
            url = Config.base_url+i["href"] if i["href"] else ""
            break
        for j in link.find(attrs={"class": "action-item votenum-mobile zm-item-vote-count js-openVoteDialog"}):
            vote = j.text
            break
        res.append({"title": title, "url": url, "vote": vote})
    try:
        res.sort(key=lambda x: int(x["vote"]), reverse=True)
    except Exception as e:
        logging.DEBUG("[SORT][BUG|{}]".format(str(e)))
        res = res
    return res


def get_search_url(content):
    """
    :param content: movie html file
    :return: return a sorted list contains all search url
    """

    res = []
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all(attrs={"class": "list_so"}):
        for i in link.find_all("dd"):
            url, movie_id = None, None
            for j in i.find("strong"):
                movie_ids = re.search("\d+", j["href"])
                try:
                    movie_id = movie_ids.group(0)
                except Exception as e:
                    logging.DEBUG("[RE|GROUP][URL|{}][BUG|{}]".format(j["href"], str(e)))
                url = Config.movie_base_url + j["href"]
            res.append((url, movie_id))
    return res


def deal_movie_content(content):
    """
    :param content:
    :return: return a list including movie detail
    """

    soup = BeautifulSoup(content, "html.parser")
    title, year, desc, kind, zone, language, actor = None, None, None, None, None, None, None

    # movie detail
    for link in soup.find_all(attrs={"class": "vod_intro rt"}):
        for i in link.find("h1"):
            title = i
            break
        for i in link.find(attrs={"class": "year"}):
            year = str(i).replace(" ", "")
            if year.startswith("("):
                year = year[1:-1]
        n = 0
        for i in link.find("dl"):
            if n == 5:
                kind = i.text
            if n == 7:
                zone = i.text
            if n == 9:
                language = i.text
            if n == 13:
                actor = i.text
            n += 1
    for link in soup.find_all(attrs={"class": "des"}):
        for i in link.find_all("div"):
            desc = i.text
            break
    return {
        "title": title,
        "year": year,
        "kind": kind,
        "zone": zone,
        "language": language,
        "actor": actor,
        "description": desc,
        "magnets": []
    }


def deal_movie_download(content):
    """
    :param content:
    :return:
    """
    res = []
    soup = BeautifulSoup(content, "html.parser")
    name, magnet = None, None

    for link in soup.find_all(attrs={"class": "p_list"}):
        for item in link.find_all("li"):
            for i in item.find_all(attrs={"class": "ico_1"}):
                name = i["title"]
            for i in item.find_all(attrs={"class": "d1"}):
                magnet = i["href"]
            if name is None or magnet is None:
                continue
            res.append({"name": name, "magnet": magnet})
    return res


def deal_torrent_content(content):
    """
    :param content:
    :return:
    """

    res = []
    soup = BeautifulSoup(content, "html.parser")
    name, size, numbers, magnet, torrent = None, None, None, None, None
    for link in soup.find_all(attrs={"class": "mlist"}):
        for item in link.find_all("li"):
            for i in item.find_all(attrs={"class": "T1"}):
                name = i.text.strip(" ")
            for i in item.find_all(attrs={"class": "BotInfo"}):
                n = 0
                for j in i.find_all("span"):
                    if n == 0:
                        size = j.text.strip(" ")
                    elif n == 1:
                        numbers = j.text.replace(" ", "")
                    else:
                        break
                    n += 1
            for i in item.find_all(attrs={"class": "dInfo"}):
                n = 0
                for j in i.find_all("a"):
                    if n == 0:
                        magnet = j["href"].strip(" ")
                    elif n == 1:
                        torrent = j["href"].strip(" ")
                    else:
                        break
                    n += 1
            res.append({"name": name, "size": size, "numbers": numbers, "magnet": magnet, "torrent": torrent})
    return res


def deal_douban_content(content):
    """
    :param content: douban search result
    :return 
    """
    res = []
    soup = BeautifulSoup(content, "html.parser")
    for link in soup.find_all(attrs={"class": "result"}):
        for item in link.find_all(attrs={"class": "title"}):
            for i in item.find_all("h3"):
                for j in i.find_all("span"):
                    kind = j.text.replace(" ", "").strip("\n\r")[1:-1]
                    break
                for j in i.find_all("a"):
                    url = j["href"]
                if kind in ["小组", "小站"]:
                    continue
                res.append({"kind": kind, "url": url})
    return res


def deal_douban_detail(kind, content):
    """
    """

    res = []

    soup = BeautifulSoup(content, "html.parser")
    if kind == "电影":
        for link in soup.find_all(attrs={"id": "content"}):
            for item in link.find_all("h1"):
                for i in item.find_all(attrs={"property": "v:itemreviewed"}):
                    title = i.text
                for i in item.find_all(attrs={"class": "year"}):
                    year = i.text[1:-1]
            for item in link.find_all(attrs={"id": "mainpic"}):
                for i in item.find_all("img"):
                    pic = i["src"]
                    break
                break
            for item in link.find_all(attrs={"id": "info"}):
                for i in item.find_all("span"):
                    pass
            break
        pass
    elif kind == "游戏":
        pass
    elif kind == "书籍":
        pass


