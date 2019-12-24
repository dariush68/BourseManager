from django.conf.urls import url
from . import views

app_name = 'bourseapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # category urls
    url(r'^category-list/$', views.category_list, name='category-list'),
    url(r'^(?P<category_id>[0-9]+)/category-detail/$', views.category_detail, name='category-detail'),

    # company urls
    url(r'^company-list/$', views.company_list, name='company-list'),
    url(r'^(?P<company_id>[0-9]+)/company-detail/$', views.company_detail, name='company-detail'),

    # new urls
    url(r'^news-list/$', views.new_list, name='news-list'),
    url(r'^(?P<news_id>[0-9]+)/news-detail/$', views.news_detail, name='news-detail'),

    # technical urls
    url(r'^technical-list/$', views.technical_list, name='technical-list'),
    url(r'^(?P<technical_id>[0-9]+)/technical-detail/$', views.technical_detail, name='technical-detail'),

    # fundamental urls
    url(r'^fundamental-list/$', views.fundamental_list, name='fundamental-list'),
    url(r'^(?P<fundamental_id>[0-9]+)/fundamental-detail/$', views.fundamental_detail, name='fundamental-detail'),

]
