= User Media

This folder will contain the files uploaded through the Django application in
development. 

These files will not be copied to the server during the normal deployment cycle.

deploy user media:
- fab [prod|staging|dev].deploy_static_media

