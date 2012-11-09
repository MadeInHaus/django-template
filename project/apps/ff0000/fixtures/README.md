# auth.user

Development and test environments come with a pre-installed admin/admin user.
Staging and production don't, and Django asks for admin to be created when 
synchronizing the database for the first time.

# sites.site

All environments come with a default "http://example.com:8000" site installed.
This site is automatically updated when deploying to a remote machine using
fabric.
