from django.conf.urls import url
from . import views

app_name = 'bourseapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # category urls
    url(r'^category-list/$', views.category_list, name='category-list'),

    # company urls
    url(r'^company-list/$', views.company_list, name='company-list'),

    # new urls
    url(r'^news-list/$', views.new_list, name='news-list'),

]
