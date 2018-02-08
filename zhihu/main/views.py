import json
import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from .util import deal_content

from zhihu.config import Config

# Create your views here.


class Search(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params.get("keywords")
        if not data:
            return HttpResponse(json.dumps({"error": "no params"}))
        res = requests.get(url=Config.url_search+data, headers=Config.headers)
        result = deal_content(res.content.decode())
        return HttpResponse(json.dumps(result))

