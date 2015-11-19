import datetime
from django.contrib.gis.db import models

class Article(models.Model):
    sourceid = models.CharField(max_length=30, unique=True)
    date = models.DateTimeField()
    coords = models.GeometryField()
    headline = models.CharField(max_length=200)
    abstract = models.CharField(max_length=500, blank=True)
    byline = models.CharField(max_length=100)
    articlecategory = models.CharField(max_length=28)
    url = models.URLField(max_length=300, unique=True)
    retweetcount = models.IntegerField()
    sharecount = models.IntegerField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.headline

class Keyword(models.Model):
    article = models.ForeignKey(Article, related_name='keywords', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=80)

    def __unicode__(self):
        return '%s' % (self.keyword)

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    url = models.URLField(max_length=500)

    def __unicode__(self):
        return '%s' % (self.keyword)

# class Author(models.Model):
#     article = models.ForeignKey(Article, related_name='authors', on_delete=models.CASCADE)
#     first = models.CharField(max_length=30)
#     last = models.CharField(max_length=30)

#     def __unicode__(self):
#         return '%s, %s' % (self.last, self.first)

class RetweetCount(models.Model):
    article = models.ForeignKey(Article, related_name='retweetcounts', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.date.today)
    retweetcount = models.IntegerField()

    def __unicode__(self):
        return '%s: %d' % (self.date, self.retweetcount)

class FacebookCount(models.Model):
    article = models.ForeignKey(Article, related_name='facebookcounts', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.date.today)
    likecount = models.IntegerField()
    commentcount = models.IntegerField()
    sharecount = models.IntegerField()
    clickcount = models.IntegerField()

    def __unicode__(self):
        return '%s: %d' % (self.date, self.retweetcount)
