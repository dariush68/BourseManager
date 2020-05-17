
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from bourseapp import views as core_views
from bourseapp import sitemaps

sitemaps = {
    # 'static': sitemaps.StaticViewSitemap,
    'category': sitemaps.CategorySitemap,
    'company': sitemaps.CompanySitemap,
    'news': sitemaps.NewsSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    # website urls
    url(r'^', include('bourseapp.urls')),

    # api urls
    url(r'^api/bourse/', include(('bourseapp.api.urls', 'api-bourseapp'), namespace='api-bourseapp')),

    # jwt_simple token urls
    # url(r'^api/auth/login/$', obtain_jwt_token, name='api-login'),
    url(r'^api/token/$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/token/verify/$', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    # Add Django site authentication urls (for login, logout, password management)
    # accounts/ login/ [name='login']
    # accounts/ logout/ [name='logout']
    # accounts/ password_change/ [name='password_change']
    # accounts/ password_change/done/ [name='password_change_done']
    # accounts/ password_reset/ [name='password_reset']
    # accounts/ password_reset/done/ [name='password_reset_done']
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/ reset/done/ [name='password_reset_complete']
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^signup/$', core_views.signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

