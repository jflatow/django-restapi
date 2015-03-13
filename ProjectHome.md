Initially this project was meant as an improvements proposal for the existing django-rest-interface project, which was a good start but had some issues. The initial discussion can be found [here](http://groups.google.com/group/django-developers/browse_thread/thread/60ce1a298b595918/).

Nothing ever happened with the issue as posted to the existing project, and since there still seems a need for this functionality, this project now exists.

Here is a very simple example of how you might create an API for a Publication model, using Django's builtin JSON serializer and HTTP basic authentication:

```

@authenticate(HttpBasicAuthentication()) 
class PublicationCollection(ModelCollection): 
     allowed_methods = ('GET', 'POST') 
Publications = PublicationCollection(Publication, JSONSerDes) 

```

You could then put something like this in your urls.py:

```

urlpatterns = patterns('', (r'^publications(/(?P<id>.*))?$', Publications)) 

```

See a more detailed [example](http://code.google.com/p/django-restapi/wiki/Examples).