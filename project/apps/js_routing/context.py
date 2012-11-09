from django.core.urlresolvers import resolve
from django.conf import settings

from functions import build_js_route_map

js_route_map = build_js_route_map()
def js_config(request):
    """
    Uses js_route_map to map the url being processed
    to the routes that were declared by the front end.

    This can either be done using named url patterns or
    a straight up url match. If a match is found
    the config object is added to the context.
    """
    match_key = None

    # Rebuild the map everytime in debug mode
    if settings.DEBUG:
        local_route_map = build_js_route_map()
    else:
        local_route_map = js_route_map

    if request.path_info in local_route_map:
        match_key = request.path_info
    else:
        try:
            match = resolve(request.path_info)
            if match and match.url_name in local_route_map:
                match_key = match.url_name
        except:
            pass

    if match_key:
        return {
            'page_config' : local_route_map[match_key]
        }

    return {}

def base_template(request):
    """
    This context processor sets the base_template
    that should be used as the base template.

    Allows for different bases for ajax and html
    requests.
    """

    base_ajax = getattr(settings, 'BASE_AJAX_TEMPLATE', 'base_ajax.html')
    base_html = getattr(settings, 'BASE_HTML_TEMPLATE', 'base.html')

    if request.is_ajax():
        template = base_ajax
    else:
        template = base_html
    return {
        'base_template' : template
    }
