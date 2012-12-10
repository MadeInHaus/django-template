## Frontend Dev notes ##


Haus boilerplate enables django-require which automatically runs the JS compile process when you run a collect static.  To test this run the following:


    fab vagrant.collectstatic

This process will compile all of the Javascript.

create a file at project/settings/hosts/local_settings.py  

Inside this file add:
    
    DEBUG = False
    SERVE_STATIC = True

You need to shut off DEBUG so that the staticfiles app doesn't inject a route at /static/.  You then enable SERVE_STATIC = True to inject a route for the collected-static directory.  

Keep in mind, to have the application pull the uncompiled files, you need to flip those variables to the inverse.  
