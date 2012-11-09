# This context processor allows templates to simply access Django settings
# For exaxmple: {% if settings.ENVIRONMENT == 'development' %} {% endif %}
# Only the settings specified in settings.SETTINGS will be passed
from django.conf import settings as _settings

def settings(request):

    values = {}
    try:
        for v in _settings.VIEW_SETTINGS:
            values[v] = getattr(_settings, v)
    except AttributeError:  # no SETTINGS in Django settings
        pass
    return {'settings': values}
