from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^api/search_result', views.Search.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
