from django.conf.urls import url
from . import views
# 给URL模式规定命名空间，指向comments。最后在根目录urls下包涵此文件
app_name = 'comments'
urlpatterns = [
    url(r'^comment/article/(?P<article_pk>[0-9]+)/$', views.article_comment, name='article_comment'),
]