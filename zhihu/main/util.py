import logging
from bs4 import BeautifulSoup
from zhihu.config import Config


def deal_content(content):
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
