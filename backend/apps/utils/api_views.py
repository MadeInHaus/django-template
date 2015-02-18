from django.shortcuts import render_to_response
# Import the tastypie.api.Api object with which your api resources are registered. 
from backend.urls import v1_api as api

def api_profile(request, resource):
    """ Allows easy profiling of API requests with django-debug-toolbar. """
    context = {}
    resource = resource.strip('/')
    resource = api.canonical_resource_for(resource)
    response = resource.get_list(request)
    context['api_response'] = response
    response = render_to_response('utils/api_profile.html', context)
    print response['content-type']
    return response