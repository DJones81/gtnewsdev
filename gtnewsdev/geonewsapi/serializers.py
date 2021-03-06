from gtnewsdev.geonewsapi.models import Article, Keyword, Image, RetweetCount, FacebookCount
from rest_framework import serializers
from rest_framework_gis import serializers as geoserializers
from django.contrib.gis import geos

import math
# from pprint import pprint

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('keyword', )

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url', )

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
    images = ImageSerializer(many=True)
    retweetcounts = RetweetCountSerializer(many=True)
    facebookcounts = FacebookCountSerializer(many=True)

    class Meta:
        model = Article
        fields = ('pk', 'sourceid', 'date', 'coords', 'headline', 'abstract', 'byline', 'category', 'sectionname', 'url', 'retweetcount', 'sharecount', 'keywords', 'images', 'retweetcounts', 'facebookcounts')
        geo_field = 'coords'

    def create(self, validated_data):
        keywords_data = validated_data.pop('keywords')
        images_data = validated_data.pop('images')
        retweetcounts_data = validated_data.pop('retweetcounts')
        facebookcounts_data = validated_data.pop('facebookcounts')
        article = Article.objects.create(**validated_data)
        for keyword_data in keywords_data:
            Keyword.objects.create(article=article, **keyword_data)
        for image_data in images_data:
            Image.objects.create(article=article, **image_data)
        for retweetcount_data in retweetcounts_data:
            RetweetCount.objects.create(article=article, **retweetcount_data)
        for facebookcount_data in facebookcounts_data:
            FacebookCount.objects.create(article=article, **facebookcount_data)
        return article

    def update(self, instance, validated_data):
        keywordlist = validated_data.pop('keywords')
        imagelist = validated_data.pop('images')
        retweetcountlist = validated_data.pop('retweetcounts')
        facebookcountlist = validated_data.pop('facebookcounts')
        Article.objects.filter(pk=instance.id).update(**validated_data)
        keywords = [keyword['keyword'] for keyword in keywordlist]
        for keyword in instance.keywords.all():
            if keyword.keyword not in keywords:
                Keyword.objects.get(pk=keyword.id).delete()
        for keyword in keywordlist:
            Keyword.objects.get_or_create(article=instance, **keyword)

        urls = [image['url'] for image in imagelist]
        for image in instance.images.all():
            if image.url not in urls:
                Image.objects.get(pk=image.id).delete()
        for image in imagelist:
            Image.objects.get_or_create(article=instance, **image)
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
    pinsize = serializers.SerializerMethodField('size')

    # def category_map(self, article):
    #     return {
    #         'Science': 'science',
    #         'Health': 'health',
    #         'Job Market': 'economy',
    #         'World': 'world',
    #         'Workplace': 'conflict'
    #     }.get(article.articlecategory, 'world')

    def size(self, article):
        # pprint(getattr(self.context['view'], 'max_retweetcount'))
        statcounts = getattr(self.context['view'], 'statcounts')
        # pprint(statcounts)
        pinsize = {}
        pinsize['twitter'] = 1.0 if statcounts['retweet']['max']==0 else 0.8*(article.retweetcount/statcounts['retweet']['max'])+0.2 #0.9*(article.retweetcount-statcounts['retweet']['min'])/statcounts['retweet']['maxmin']+0.1
        pinsize['facebook'] = 1.0 if statcounts['share']['max']==0 else 0.8*(article.sharecount/statcounts['share']['max'])+0.2 #0.9*(article.sharecount-statcounts['share']['min'])/statcounts['share']['maxmin']+0.1
        pinsize['both'] = 1.0 if statcounts['both']['max']==0 else 0.8*((article.retweetcount+article.sharecount)/statcounts['both']['max'])+0.2 #0.9*((article.retweetcount+article.sharecount)-statcounts['both']['min'])/statcounts['both']['maxmin']+0.1
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

    class Meta:
        model = Article
        fields = ('pk', 'date', 'coords', 'pinsize', 'headline', 'abstract', 'byline', 'url', 'category', 'retweetcount', 'sharecount')
        geo_field = 'coords'

class PinDetailSerializer(serializers.ModelSerializer):
    coords = geoserializers.GeometryField(label=('coordinates'))
    keywords = KeywordSerializer(many=True)
    images = ImageSerializer(many=True)
    retweetcounts = RetweetCountSerializer(many=True)
    facebookcounts = FacebookCountSerializer(many=True)

    # def category_map(self, article):
    #     return {
    #         'Science': 'science',
    #         'Health': 'health',
    #         'Job Market': 'economy',
    #         'World': 'world',
    #         'Workplace': 'conflict'
    #     }.get(article.articlecategory, 'world')

    class Meta:
        model = Article
        fields = ('pk', 'date', 'coords', 'headline', 'abstract', 'byline', 'url', 'category', 'retweetcount', 'sharecount', 'keywords', 'retweetcounts', 'facebookcounts', 'images')
        geo_field = 'coords'