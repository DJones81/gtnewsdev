from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend,  OrderingFilter
from rest_framework_word_filter import FullWordSearchFilter
from rest_framework_gis.filters import InBBoxFilter

from django_filters import FilterSet, DateTimeFilter, NumberFilter

from gtnewsdev.geonewsapi.models import Article
from gtnewsdev.geonewsapi.serializers import ArticleSerializer, PinSerializer

class ArticleFilter(FilterSet):
    start_date = DateTimeFilter(name='date',lookup_type='gte')
    end_date = DateTimeFilter(name='date',lookup_type='lte')
    min_retweetcount = NumberFilter(name='retweetcount',lookup_type='gte')
    min_sharecount = NumberFilter(name='sharecount',lookup_type='gte')

    class Meta:
        model = Article
        fields = ['start_date', 'end_date', 'sourceid', 'url', 'min_retweetcount', 'min_sharecount']

class PinFilter(FilterSet):
    start_date = DateTimeFilter(name='date',lookup_type='gte')
    end_date = DateTimeFilter(name='date',lookup_type='lte')
    min_retweetcount = NumberFilter(name='retweetcount',lookup_type='gte')
    min_sharecount = NumberFilter(name='sharecount',lookup_type='gte')

    class Meta:
        model = Article
        fields = ['start_date', 'end_date', 'min_retweetcount', 'min_sharecount']

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects
    serializer_class = ArticleSerializer
    bbox_filter_field = 'coords'
    word_fields = ('headline','abstract','keywords__keyword') #,'authors__first','authors__last')
    filter_class = ArticleFilter
    filter_backends = (DjangoFilterBackend, FullWordSearchFilter, InBBoxFilter, OrderingFilter)
    ordering_fields = ('retweetcount', 'sharecount', 'date', 'id')
    bbox_filter_include_overlapping = True

    # @list_route(methods=['get'], serializer_class=PinSerializer)
    # def pins(self, request):
    #     serializer = self.get_serializer(self.list(request).get_queryset(), many=True)
    #     return Response(serializer.data)

class PinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.exclude(coords__exact = "{ \"type\": \"Point\", \"coordinates\": [ 0, 0 ] }")
    serializer_class = PinSerializer
    bbox_filter_field = 'coords'
    word_fields = ('headline','abstract','keywords__keyword') #,'authors__first','authors__last')
    filter_class = PinFilter
    filter_backends = (DjangoFilterBackend, FullWordSearchFilter, InBBoxFilter, OrderingFilter)
    ordering_fields = ('retweetcount', 'sharecount', 'date')
    bbox_filter_include_overlapping = True

#@api_view(['GET', 'POST'])
#def article_list(request):
#	if request.method == 'GET':
#		articles = Article.objects.all()
#		serializer = ArticleSerializer(articles, many=True)
#		return Response(serializer.data)
#	elif request.method == 'POST':
#		serializer = ArticleSerializer(data=request.DATA)
#		if serializer.is_valid():
#			serializer.save()
#			return Response(serializer.data, status=status.HTTP_201_CREATED)
#		else:
#			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#@api_view(['GET', 'PUT', 'DELETE'])
#def article_detail(request, pk):
#    try:
#        task = Article.objects.get(pk=pk)
#    except Article.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#
#    if request.method == 'GET':
#        serializer = ArticleSerializer(task)
#        return Response(serializer.data)
#
#    elif request.method == 'PUT':
#        serializer = ArticleSerializer(task, data=request.DATA)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        else:
#            return Response(
#                serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    elif request.method == 'DELETE':
#        Article.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
