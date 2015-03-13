# Introduction #

You can create a RESTful API for your models by creating Resource and Collection objects which you can map urls to, much like you would for any other type of django view.


# Details #

## models.py ##

```

from django.db import models

class Publication(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
	return self.title

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    def __unicode__(self):
        return self.headline

```

## views.py ##

```

from django.contrib.restapi.serdes import JSONSerDes, XMLSerDes
from django.contrib.restapi.models import ModelCollection, ModelObjectResource
from django.contrib.restapi.auth import authenticate, deauthenticate, HttpBasicAuthentication, HttpDigestAuthentication

from .models import Publication, Article

#                                                                                                                                                                                                                                                                                                                                                                                                                                     
# create/read publications JSON API                                                                                                                                                                                                                                                                                                                                                                                                   
#                                                                                                                                                                                                                                                                                                                                                                                                                                     
class PublicationCollection(ModelCollection):
    allowed_methods = ('GET', 'POST')

Publications = PublicationCollection(Publication, JSONSerDes)

#                                                                                                                                                                                                                                                                                                                                                                                                                                     
# create/read/delete articles XML API w/ some authentication                                                                                                                                                                                                                                                                                                                                                                          
#                                                                                                                                                                                                                                                                                                                                                                                                                                     
@authenticate(HttpBasicAuthentication())
class ArticleObject(ModelObjectResource):
    allowed_methods = ('GET', 'DELETE') # turn delete on for individual articles                                                                                                                                                                                                                                                                                                                                                      

    @deauthenticate
    def read(self, request, *args, **kwargs):
	return self.__super.read(request, *args, **kwargs)

    @authenticate(HttpDigestAuthentication(lambda x, y: True))
    def delete(self, request, *args, **kwargs):
	return self.__super.delete(request, *args, **kwargs)

@authenticate(HttpBasicAuthentication())
class ArticleCollection(ModelCollection):
    allowed_methods = ('GET', 'POST') # post to the collection                                                                                                                                                                                                                                                                                                                                                                        

Articles = ArticleCollection(Article, XMLSerDes, ArticleObject)

```

## urls.py ##

```

from django.conf.urls.defaults import *
from .views import Publications, Articles

urlpatterns = patterns('',
                       (r'^publications(/(?P<id>.*))?$', Publications),
                       (r'^articles(/(?P<id>.*))?$', Articles),
                       )

```