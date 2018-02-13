from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'zhihu/search_result', views.SearchZhihu.as_view()),
    url(r"movie/search_result", views.SearchMovie.as_view()),
    url(r"torrent/search_result", views.SearchTorrent.as_view()),
    url(r"douban/search_result", views.SearchDouban.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
