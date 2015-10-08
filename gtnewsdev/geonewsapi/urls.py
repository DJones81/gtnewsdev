from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from gtnewsdev.geonewsapi.views import ArticleViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = patterns(
    'gtnewsdev.geonewsapi.views',
    url(r'^', include(router.urls)),
#    url(r'^articles/$', 'article_list', name='article_list'),
#    url(r'^articles/(?P<pk>[0-9]+)$', 'article_detail', name='article_detail'),
)
