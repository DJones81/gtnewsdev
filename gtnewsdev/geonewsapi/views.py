from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import DjangoFilterBackend, SearchFilter, OrderingFilter
# from rest_framework_word_filter import FullWordSearchFilter
from rest_framework_gis.filters import InBBoxFilter

from django_filters import FilterSet, DateTimeFilter, NumberFilter, Filter
from django_filters.fields import Lookup

from gtnewsdev.geonewsapi.models import Article
from gtnewsdev.geonewsapi.serializers import ArticleSerializer, PinSerializer, PinDetailSerializer

from django.db.models import Max, Min, F # Avg, StdDev

# from pprint import pprint

class ListFilter(Filter):
    def filter(self, qs, value):
        value_list = value.split(u',')
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))

class ArticleFilter(FilterSet):
    category = ListFilter(name='category')
    start_date = DateTimeFilter(name='date',lookup_type='gte')
    end_date = DateTimeFilter(name='date',lookup_type='lte')
    min_retweetcount = NumberFilter(name='retweetcount',lookup_type='gte')
    min_sharecount = NumberFilter(name='sharecount',lookup_type='gte')

    class Meta:
        model = Article
        fields = ['start_date', 'end_date', 'sourceid', 'url', 'min_retweetcount', 'min_sharecount', 'category']

class PinFilter(FilterSet):
    category = ListFilter(name='category')
    start_date = DateTimeFilter(name='date',lookup_type='gte')
    end_date = DateTimeFilter(name='date',lookup_type='lte')
    min_retweetcount = NumberFilter(name='retweetcount',lookup_type='gte')
    min_sharecount = NumberFilter(name='sharecount',lookup_type='gte')

    class Meta:
        model = Article
        fields = ['start_date', 'end_date', 'min_retweetcount', 'min_sharecount', 'category']

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.distinct()
    serializer_class = ArticleSerializer
    bbox_filter_field = 'coords'
    search_fields = ('headline','abstract','byline','keywords__keyword') #,'authors__first','authors__last')
    filter_class = ArticleFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, InBBoxFilter, OrderingFilter)
    ordering_fields = ('retweetcount', 'sharecount', 'date', 'id')
    bbox_filter_include_overlapping = True

    # @list_route(methods=['get'], serializer_class=PinSerializer)
    # def pins(self, request):
    #     serializer = self.get_serializer(self.list(request).get_queryset(), many=True)
    #     return Response(serializer.data)

class PinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.exclude(coords__exact = "{ \"type\": \"Point\", \"coordinates\": [ 0, 0 ] }").distinct()
    bbox_filter_field = 'coords'
    search_fields = ('headline','abstract','byline','keywords__keyword') #,'authors__first','authors__last')
    filter_class = PinFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, InBBoxFilter, OrderingFilter)
    ordering_fields = ('retweetcount', 'sharecount', 'date')
    bbox_filter_include_overlapping = True

    serializers = {
        'list':    PinSerializer,
        'retrieve':  PinDetailSerializer,
        'default': PinSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_queryset(self):
        query_params = self.request.query_params.copy()
        start_date = query_params.get('start_date', '').replace('T',' ').replace('Z','')
        end_date = query_params.get('end_date', '').replace('T',' ').replace('Z','')
        query_params.__setitem__('start_date', start_date)
        query_params.__setitem__('end_date', end_date)
        self.request._request.GET = query_params
        return self.queryset

    def get_serializer(self, *args, **kwargs):
        # kwargs.update(self.serializer_kwargs)
        # serializer = super(ArticleViewSet, self).get_serializer(instance, data, many, partial)
        # pprint(getattr(self, 'max_retweetcount'))
        
        # setattr(instance, 'max_retweetcount', data.filtered_set().aggregate(Max('retweetcount')))
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        # print('\n get serializer self')
        # pprint(vars(self))
        # print('\nargs')
        # pprint(args)
        # print('\n kwargs')
        # pprint(dir(kwargs['context']['view']))
        resultant = self.filter_queryset(self.queryset)
        statcounts = {'retweet': {}, 'share': {}, 'both': {}}

        statcounts['retweet']['max'] = resultant.aggregate(Max('retweetcount'))['retweetcount__max']
        statcounts['share']['max'] = resultant.aggregate(Max('sharecount'))['sharecount__max']
        statcounts['both']['max'] = resultant.annotate(sum=F('retweetcount') + F('sharecount')).aggregate(Max('sum'))['sum__max']

        # maxmin_retweetcount = resultant.aggregate(Max('retweetcount'))['retweetcount__max']-resultant.aggregate(Min('retweetcount'))['retweetcount__min']
        # statcounts['retweet']['maxmin'] = maxmin_retweetcount if (maxmin_retweetcount!=0) else 1
        # maxmin_sharecount = resultant.aggregate(Max('sharecount'))['sharecount__max']-resultant.aggregate(Min('sharecount'))['sharecount__min']
        # statcounts['share']['maxmin'] = maxmin_sharecount if (maxmin_sharecount!=0) else 1
        # maxmin_both = resultant.annotate(sum=F('retweetcount') + F('sharecount')).aggregate(Max('sum'))['sum__max']-resultant.annotate(sum=F('retweetcount') + F('sharecount')).aggregate(Min('sum'))['sum__min']
        # statcounts['both']['maxmin'] = maxmin_both if (maxmin_both!=0) else 1
        
        # min_retweetcount = resultant.aggregate(Min('retweetcount'))['retweetcount__min']
        # statcounts['retweet'] = min_retweetcount if (min_retweetcount!=0) else 1
        # min_sharecount = resultant.aggregate(Min('sharecount'))['sharecount__min']
        # statcounts['share'] = min_sharecount if (min_sharecount!=0) else 1
        # min_both = resultant.annotate(sum=F('retweetcount') + F('sharecount')).aggregate(Min('sum'))['sum__min']
        # statcounts['both'] = min_both if (min_both!=0) else 1

        # avg_retweetcount = resultant.aggregate(Avg('retweetcount'))['retweetcount__avg']
        # statcounts['retweet'] = avg_retweetcount if (avg_retweetcount!=0) else 1
        # avg_sharecount = resultant.aggregate(Avg('sharecount'))['sharecount__avg']
        # statcounts['share'] = avg_sharecount if (avg_sharecount!=0) else 1
        # avg_both = resultant.annotate(sum=F('retweetcount') + F('sharecount')).aggregate(Avg('sum'))['sum__avg']
        # statcounts['both'] = avg_both if (avg_both!=0) else 1

        # stddev_retweetcount = resultant.aggregate(StdDev('retweetcount'))['retweetcount__stddev']
        # statcounts['retweet'] = stddev_retweetcount if (stddev_retweetcount!=0) else 1
        # stddev_sharecount = resultant.aggregate(StdDev('sharecount'))['sharecount__stddev']
        # statcounts['share'] = stddev_sharecount if (stddev_sharecount!=0) else 1
        # stddev_both = resultant.annotate(sum=F('retweetcount') + F('sharecount')).aggregate(StdDev('sum'))['sum__stddev']
        # statcounts['both'] = stddev_both if (stddev_both!=0) else 1
        setattr(self, 'statcounts', statcounts)
        return serializer_class(*args, **kwargs)