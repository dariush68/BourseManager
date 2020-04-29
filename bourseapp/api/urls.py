from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import *

app_name = 'api-bourseapp'

urlpatterns = [
    url(r'^Category$', views.CategoryAPIView.as_view(), name='post-listcreate'),
    # url(r'^Category/(?P<pk>\d+)/$', views.CategoryRudView.as_view(), name='post-rud'),

    url(r'^Symbols$', views.SymbolsAPIView.as_view(), name='symbols-view'),
    url(r'^user-list$', views.UserList.as_view(), name='user-list'),

    url(r'^ChatMessage$', views.ChatMessageAPIView.as_view(), name='post-listcreate-chatMessage'),
    url(r'^ChatMessage/(?P<pk>\d+)/$', views.ChatMessageRudView.as_view(), name='post-rud-chatMessage'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
