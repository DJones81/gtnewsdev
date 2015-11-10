from gtnewsdev.geonewsapi.models import Article, Keyword, RetweetCount
from rest_framework import serializers
from rest_framework_gis import serializers as geoserializers
from django.contrib.gis import geos

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
#        print >>sys.stderr, validated_data
        keywords_data = validated_data.pop('keywords')
        # authors_data = validated_data.pop('authors')
        retweetcounts_data = validated_data.pop('retweetcounts')
        article = Article.objects.create(**validated_data)
        for keyword_data in keywords_data:
            Keyword.objects.create(article=article, **keyword_data)
        # for author_data in authors_data:
            # Author.objects.create(article=article, **author_data)
        for retweetcount_data in retweetcounts_data:
            RetweetCount.objects.create(article=article, **retweetcount_data)
        return article

    def update(self, instance, validated_data):
#        print >>sys.stderr, instance
#        print >>sys.stderr, validated_data
        keywordlist = validated_data.pop('keywords')
        # authorlist = validated_data.pop('authors')
        retweetcountlist = validated_data.pop('retweetcounts')
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
        retweetcounts = [retweetcount['retweetcount'] for retweetcount in retweetcountlist]
        for retweetcount in instance.retweetcounts.all():
            if retweetcount.retweetcount not in retweetcounts:
                RetweetCount.objects.get(pk=retweetcount.id).delete()
        for retweetcount in retweetcountlist:
            RetweetCount.objects.get_or_create(article=instance, **retweetcount)
        return instance

class PinSerializer(serializers.ModelSerializer):
    coords = geoserializers.GeometryField(label=('coordinates'))
    category = serializers.SerializerMethodField('category_map')
    isgeolocated = serializers.SerializerMethodField('islocated')
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

    def islocated(self, article):
        return not article.coords.equals(geos.Point(0,0))

    def size(self, article):
        return 1


    # retweetcount = serializers.SlugRelatedField(
    #         queryset=Article.objects.retweetcounts.latest('date'),
    #         read_only=true,
    #         slug_field='retweetcount'
    #     )

    class Meta:
        model = Article
        fields = ('pk', 'date', 'coords', 'pinsize', 'isgeolocated', 'headline', 'abstract', 'byline', 'url', 'category', 'retweetcount', 'sharecount')
        geo_field = 'coords'
