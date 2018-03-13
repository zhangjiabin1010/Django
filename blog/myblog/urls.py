from django.conf.urls import url
from . import views
import re

# 指定这个urls.pyshi属于‘myblog’应用的，这种技术叫视图函数的命名空间
app_name = 'myblog'
urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # as_view 方法,将类视图转换为函数视图
    # url(r'^category/(?P<pk>[0-9]+)/$',views.category, name='category'),
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(), name='category'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^tag/(?P<pk>[0-9]+)/$',views.tag, name='tag'),
    url(r'^search/$', views.search, name='search'),

]
