## Install required python libs Fabric and Boto
```
sudo easy_install fabric
sudo easy_install boto
```


## Install VirtualBox

[download](https://www.virtualbox.org/wiki/Downloads) virtualbox
install package


## Install Vagrant

[installation instructions](http://vagrantup.com/v1/docs/getting-started/index.html)

[downloads](http://downloads.vagrantup.com/)


## Initialize and start server
```
vagrant up
fab vagrant.initdb
fab vagrant.runserver
```

view the site running at: [localhost:8080](http://localhost:8080/)


## Heroku setup
- install heroku [toolbelt](https://toolbelt.heroku.com/)
- be sure to login and generate a new key if prompted `heroku login`
- add remotes for app,  based on the heroku app names which can be found in app_info.json in the project root:
```
fab remotes
```

## Local Dev settings
create a file in: 
project/settings/hosts/local_settings.py

This file overrides settings and is ignored by git automatically.


## DELETE ME AFTER SETUP ##
if you want to switch to mysql from postgres:
* puppet/app.pp
    * delete include app::postgresql
    * uncomment include app::mysql
* fabfile/vagrant.py
    * in function def resetdb(): comment out postgres lines, and uncomment mysql lines    
* project/settings/base.py
    * change 'ENGINE': 'django.db.backends.postgresql_psycopg2', to  'ENGINE': 'django.db.backends.mysql', 

