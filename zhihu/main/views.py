import json
import requests
from threading import Thread
from django.http import HttpResponse
from rest_framework.views import APIView
from .util import (deal_zhihu_content, get_search_url, deal_movie_content, deal_movie_download, 
    deal_torrent_content, deal_douban_content, deal_douban_detail)

from zhihu.config import Config

# Create your views here.


class SearchZhihu(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params.get("keywords")
        if not data:
            return HttpResponse(json.dumps({"error": "no params"}))
        res = requests.get(url=Config.url_search+data, headers=Config.headers)
        result = deal_zhihu_content(res.content.decode())
        return HttpResponse(json.dumps(result))


class SearchMovie(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params.get("keywords")
        if not data:
            return HttpResponse(json.dumps({"error": "no params"}))
        res = requests.get(url=Config.movie_search_url.format(data))
        url_list = get_search_url(res.content)
        result, thread_list = [], []

        def _get_movie_detail(url):
            data = requests.get(url[0])
            magnet = requests.get(Config.movie_download_url.format(url[1]))
            res = deal_movie_content(data.content)
            magnets = deal_movie_download(magnet.content.decode())
            res["magnets"] = magnets
            result.append(res)

        for url in url_list:
            thread_list.append(Thread(target=_get_movie_detail, args=(url,)))
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        return HttpResponse(json.dumps(result))


class SearchTorrent(APIView):
    """
    search torrent
    """

    def get(self, request, *args, **kwargs):
        data = request.query_params.get("keywords")
        if not data:
            return HttpResponse(json.dumps({"error": "no params"}))
        res = requests.get(url=Config.torrent_search_url.format(data))
        result = deal_torrent_content(res.content)
        return HttpResponse(json.dumps(result))


class SearchDouban(APIView):
    """
    search content from douban
    """

    def get(self, request, *args, **kwargs):
        data = request.query_params.get("keywords")
        if not data:
            return HttpResponse(json.dumps({"error": "no params"}))
        res = requests.get(url=Config.douban_search_url.format(data))
        url_list = deal_douban_content(res.content.decode())
        result = []

        def _get_detail(kind, url):
            res = requests.get(url).content
            data = deal_douban_detail(kind, res)
            result.append(data)
        _get_detail(url_list[0]["kind"], url_list[0]["url"])
        # thread_list = []
        # for i in url_list:
        #     kind, url = i.get("kind"), i.get("url")
        #     thread_list.append(Thread(target=_get_detail, args=(king, url)))
        # _get_detail(url)

        return HttpResponse(json.dumps({"hello": "world"}))
        
