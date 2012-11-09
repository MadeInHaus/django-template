from django import http

from functions import get_routing_js

def routing_js(request):
    """
    View to render routing js.
    SHOULD NOT BE USED IN PRODUCTION
    """
    response = http.HttpResponse(get_routing_js())
    response['Content-Type'] = 'application/javascript'
    return response
