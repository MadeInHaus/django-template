import json
import os

from django.conf import settings
from django.template.loader import render_to_string

URL_ATTR = 'urlName'
CONFIG_ATTR = 'config'
ROUTE_ATTR = 'route'

JSON_TEMPLATE = getattr(settings, 'ROUTES_JSON_TEMPLATE', 'routes.json')
JS_TEMPLATE = getattr(settings, 'ROUTES_FULL_TEMPLATE', 'full-routes.js')
STATIC_FILE = getattr(settings, 'ROUTES_STATIC', 'config/routes.js')

def build_js_route_map():
    """
    Generates a mapping of the declared routes from
    the template 'js_routes.json' with their config
    parameters. Used by js_routing.
    """
    mapping = {}

    data = render_to_string(JSON_TEMPLATE)
    data = json.loads(data.strip())
    for route_obj in [ x["routes"] for x in data if "routes" in x ]:
        for obj in route_obj:
            if URL_ATTR in obj:
                if type(obj[URL_ATTR]) is list:
                    for key in obj[URL_ATTR]:
                        mapping[key] = obj[CONFIG_ATTR]
                else:
                    mapping[obj[URL_ATTR]] = obj[CONFIG_ATTR]
            else:
                mapping[obj[ROUTE_ATTR]] = obj[CONFIG_ATTR]

    return mapping

def get_routing_js():
    """
    Renders the full JS template
    """
    return render_to_string(JS_TEMPLATE,
                            { 'json_template' : JSON_TEMPLATE })

def build_js_file():
    """
    Renders the full JS template and then
    writes it output to a static file.
    """
    data = get_routing_js()
    base = os.path.join(settings.DEV_STATIC_ROOT, 'js')
    if os.path.exists(base):
        filename = os.path.join(base, STATIC_FILE)
        with open(filename, 'w') as fp:
            fp.write(data)
