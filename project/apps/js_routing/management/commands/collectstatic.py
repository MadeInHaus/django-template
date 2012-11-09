from django.contrib.staticfiles.management.commands.collectstatic import Command as BaseCommand

from js_routing.functions import build_js_file

class Command(BaseCommand):
    """
    Command that collects static and generates the routes js from the templates.
    """
    help = "Collect static files from apps and other locations in a single location."

    def handle_noargs(self, **options):
        build_js_file()
        super(Command, self).handle_noargs(**options)
