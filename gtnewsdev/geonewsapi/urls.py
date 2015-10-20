from collections import namedtuple

from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from gtnewsdev.geonewsapi.views import ArticleViewSet, PinViewSet

# Route = namedtuple('Route', ['url', 'mapping', 'name', 'initkwargs'])
# DynamicDetailRoute = namedtuple('DynamicDetailRoute', ['url', 'name', 'initkwargs'])
# DynamicListRoute = namedtuple('DynamicListRoute', ['url', 'name', 'initkwargs'])

# class PinRouter(DefaultRouter):
#     routes = [
#         # List route.
#         Route(
#             url=r'^{prefix}{trailing_slash}$',
#             mapping={
#                 'get': 'list',
#                 'post': 'create'
#             },
#             name='{basename}-list',
#             initkwargs={'suffix': 'List'}
#         ),
#         # Dynamically generated list routes.
#         # Generated using @list_route decorator
#         # on methods of the viewset.
#         DynamicListRoute(
#             url=r'^{prefix}/{methodname}{trailing_slash}$',
#             name='{basename}-{methodnamehyphen}',
#             initkwargs={}
#         ),
#         # Detail route.
#         Route(
#             url=r'^{prefix}/{lookup}{trailing_slash}$',
#             mapping={
#                 'get': 'retrieve',
#                 'put': 'update',
#                 'patch': 'partial_update',
#                 'delete': 'destroy'
#             },
#             name='{basename}-detail',
#             initkwargs={'suffix': 'Instance'}
#         ),
#         # Dynamically generated detail routes.
#         # Generated using @detail_route decorator on methods of the viewset.
#         DynamicDetailRoute(
#             url=r'^{prefix}/{methodname}/{lookup}{trailing_slash}$',
#             name='{basename}-{methodnamehyphen}',
#             initkwargs={}
#         ),
#     ]


router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'pins', PinViewSet)

urlpatterns = patterns(
    'gtnewsdev.geonewsapi.views',
    url(r'^', include(router.urls)),
#    url(r'^articles/$', 'article_list', name='article_list'),
#    url(r'^articles/(?P<pk>[0-9]+)$', 'article_detail', name='article_detail'),
)
