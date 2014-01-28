from django.shortcuts import render_to_response
# Import the tastypie.api.Api object with which your api resources are registered. 
from project.urls import v1_api as api

def api_profile(request, resourceboss):
    """ Allows easy profiling of API requests with django-debug-toolbar. """
    context = {}
    resourceboss = resourceboss.strip('/')
    resourceboss = api.canonical_resource_for(resourceboss)
    obj_list = resourceboss.wrap_view('dispatch_list')(request)
    #response = resource.create_response(request, obj_list)
    response = resourceboss.get_list(request)
    context['api_response'] = response
    return render_to_response('utils/api_profile.html', context)
