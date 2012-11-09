from django.core.management.commands.runserver import BaseRunserverCommand

class Command(BaseRunserverCommand):
    help = "Starts a lightweight Web server for development without automatically serving static files."
