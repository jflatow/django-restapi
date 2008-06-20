"""
Generic resource class. This was originally taken from the django-rest-interface project.
However we have completely changed the way things are done.
"""

from django.http import Http404, HttpResponse, HttpResponseNotAllowed

# add these to django.http?
class HttpResponseCreated(HttpResponse):
    status_code = 201
    
    def __init__(self, location=None):
        HttpResponse.__init__(self)
        if location:
            self['Location'] = location

class HttpResponseMultipleChoices(HttpResponse):
    status_code = 300

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self, www_authenticate):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = www_authenticate

class HttpResponseConflict(HttpResponse):
    status_code = 409

class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class MetaResource(type):
    def __init__(cls, name, bases, dict):
        setattr(cls, '_%s__super' % name, super(cls))        
        responses = {'GET': 'read',
                     'POST': 'create',
                     'PUT': 'update',
                     'DELETE': 'delete'}
        cls.responses = {}
        for method in dict.get('allowed_methods', ('GET', )):
            method = method.upper()
            if method in responses:
                cls.responses[method] = responses[method]
            else:
                raise ValueError('Unrecognized HTTP method %s' % method)

class Resource(object):
    """
    Base class for all resources
    """
    __metaclass__ = MetaResource

    def __call__(self, request, *args, **kwargs):
        try:
            return getattr(self, self.responses[request.method])(request, *args, **kwargs)
        except KeyError:
            return HttpResponseNotAllowed(self.responses)
    
    def create(self, request, *args, **kwargs):
        return HttpResponseNotImplemented()
    
    def read(self, request, *args, **kwargs):
        return HttpResponseNotImplemented()
    
    def update(self, request, *args, **kwargs):
        return HttpResponseNotImplemented()
    
    def delete(self, request, *args, **kwargs):
        return HttpResponseNotImplemented()
    
class Collection(Resource):
    """
    Abstract base class for collection resources. A collection resource is a resource
    that sometimes delegates to child resources (i.e. when called with non-empty arguments).
    """
    def __call__(self, request, *args, **kwargs):
        if filter(None, args) or filter(None, kwargs.itervalues()):
            return self.delegate(request, *args, **kwargs)
        return self.relegate(request, (), {})

    def relegate(self, request, *args, **kwargs):
        return self.__super.__call__(request, *args, **kwargs)

    def delegate(self, request, *args, **kwargs):
        """
        Map the captured arguments from the URL to a resource in this collection,
        and call the resource with appropriate arguments.
        """
        return HttpResponseNotImplemented()
