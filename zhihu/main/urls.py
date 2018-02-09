from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^api/zhihu_search_result', views.SearchZhihu.as_view()),
    url(r"api/movie_search_result", views.SearchMovie.as_view()),
    url(r"api/torrent_search_result", views.SearchTorrent.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
