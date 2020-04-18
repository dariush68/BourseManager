from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import *

app_name = 'api-bourseapp'

urlpatterns = [
    url(r'^Category$', views.CategoryAPIView.as_view(), name='post-listcreate'),
    # url(r'^Category/(?P<pk>\d+)/$', views.CategoryRudView.as_view(), name='post-rud'),

    url(r'^Symbols$', views.SymbolsAPIView.as_view(), name='symbols-view'),
    url(r'^ChartBazaar$', views.ChartView, name='chart-bazaar-view'),
    url(r'^(?P<company_id>[0-9]+)/chart-detail/$', views.chart_detail, name='chart-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
