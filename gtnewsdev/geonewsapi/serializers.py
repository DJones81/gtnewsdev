from gtnewsdev.geonewsapi.models import Article, Keyword, RetweetCount, FacebookCount
from rest_framework import serializers
from rest_framework_gis import serializers as geoserializers
from django.contrib.gis import geos

import math
# from pprint import pprint

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('keyword', )

# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ('first', 'last')

class RetweetCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetweetCount
        fields = ('date', 'retweetcount')

class FacebookCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookCount
        fields = ('date', 'likecount', 'commentcount', 'sharecount', 'clickcount')

class ArticleSerializer(serializers.ModelSerializer):
    coords = geoserializers.GeometryField(label=('coordinates'))
    keywords = KeywordSerializer(many=True)
    # authors = AuthorSerializer(many=True)
    retweetcounts = RetweetCountSerializer(many=True)
    facebookcounts = FacebookCountSerializer(many=True)
    category = serializers.CharField(source='articlecategory')

    class Meta:
        model = Article
        fields = ('pk', 'sourceid', 'date', 'coords', 'headline', 'abstract', 'byline', 'category', 'url', 'retweetcount', 'sharecount', 'keywords', 'retweetcounts', 'facebookcounts')
        geo_field = 'coords'

    def create(self, validated_data):
        # print >>sys.stderr, validated_data
        keywords_data = validated_data.pop('keywords')
        # authors_data = validated_data.pop('authors')
        retweetcounts_data = validated_data.pop('retweetcounts')
        facebookcounts_data = validated_data.pop('facebookcounts')
        article = Article.objects.create(**validated_data)
        for keyword_data in keywords_data:
            Keyword.objects.create(article=article, **keyword_data)
        # for author_data in authors_data:
            # Author.objects.create(article=article, **author_data)
        for retweetcount_data in retweetcounts_data:
            RetweetCount.objects.create(article=article, **retweetcount_data)
        for facebookcount_data in facebookcounts_data:
            FacebookCount.objects.create(article=article, **facebookcount_data)
        return article

    def update(self, instance, validated_data):
#        print >>sys.stderr, instance
#        print >>sys.stderr, validated_data
        keywordlist = validated_data.pop('keywords')
        # authorlist = validated_data.pop('authors')
        retweetcountlist = validated_data.pop('retweetcounts')
        facebookcountlist = validated_data.pop('facebookcounts')
#        logger.error('instance:')
#        logger.error(instance)
#        logger.error('validated_data:')
#        logger.error(validated_data)
#        logger.error('keywords')
#        logger.error(keywordlist)
#        instance.update(title='BBBB');
        Article.objects.filter(pk=instance.id).update(**validated_data)
        keywords = [keyword['keyword'] for keyword in keywordlist]
        for keyword in instance.keywords.all():
            if keyword.keyword not in keywords:
                Keyword.objects.get(pk=keyword.id).delete()
        for keyword in keywordlist:
            Keyword.objects.get_or_create(article=instance, **keyword)
        # authorsfirsts = [author['first'] for author in authorlist]
        # authorslasts = [author['last'] for author in authorlist]
        # for author in instance.authors.all():
        #     if not (author.first in authorsfirsts and author.last in authorslasts):
        #         Author.objects.get(pk=author.id).delete()
        # for author in authorlist:
        #     Author.objects.get_or_create(article=instance, **author)
        retweetcountids = []
        for retweetcount in retweetcountlist:
            retweetcountobj, created = RetweetCount.objects.get_or_create(article=instance, **retweetcount)
            retweetcountids.append(retweetcountobj.id)
        for retweetcount in instance.retweetcounts.all():
            if retweetcount.id not in retweetcountids:
                RetweetCount.objects.get(pk=retweetcount.id).delete()

        facebookcountids = []
        for facebookcount in facebookcountlist:
            facebookcountobj, created = FacebookCount.objects.get_or_create(article=instance, **facebookcount)
            facebookcountids.append(facebookcountobj.id)
        for facebookcount in instance.facebookcounts.all():
            if facebookcount.id not in facebookcountids:
                FacebookCount.objects.get(pk=facebookcount.id).delete()
        return instance

class PinSerializer(serializers.ModelSerializer):
    coords = geoserializers.GeometryField(label=('coordinates'))
    category = serializers.SerializerMethodField('category_map')
    #isgeolocated = serializers.SerializerMethodField('islocated')
    pinsize = serializers.SerializerMethodField('size')
    # authors = AuthorSerializer(many=True)

    def category_map(self, article):
        return {
            'Science': 'science',
            'Health': 'health',
            'Job Market': 'economy',
            'World': 'world',
            'Workplace': 'conflict'
        }.get(article.articlecategory, 'world')

    def size(self, article):
        # pprint(getattr(self.context['view'], 'max_retweetcount'))
        statcounts = getattr(self.context['view'], 'statcounts')
        # pprint(statcounts)
        pinsize = {}
        pinsize['twitter'] = math.ceil(9*(article.retweetcount-statcounts['retweet']['min'])/statcounts['retweet']['maxmin'])+1
        pinsize['facebook'] = math.ceil(9*(article.sharecount-statcounts['share']['min'])/statcounts['share']['maxmin'])+1
        pinsize['both'] = math.ceil(9*((article.retweetcount+article.sharecount)-statcounts['both']['min'])/statcounts['both']['maxmin'])+1
        # pprint(vars(self))
        # pprint(vars(self.context['request']))
        # pprint(vars(self.context['view'].request))
        # print(self.context['request'] == self.context['view'].request)
        # pprint(getattr(self.context['view'], 'max_retweetcount'))
        # pprint(self.context['view'].filter_queryset(self.context['view'].queryset).aggregate(Max('retweetcount')))
        # print('\nsize ')
        # print(self.context['request'].GET)
        # print(self.context[''])
        # print(Article.objects.filter(self.context['request'].GET))
        return pinsize


    # retweetcount = serializers.SlugRelatedField(
    #         queryset=Article.objects.retweetcounts.latest('date'),
    #         read_only=true,
    #         slug_field='retweetcount'
    #     )

    class Meta:
        model = Article
        fields = ('pk', 'date', 'coords', 'pinsize', 'headline', 'abstract', 'byline', 'url', 'category', 'retweetcount', 'sharecount')
        geo_field = 'coords'