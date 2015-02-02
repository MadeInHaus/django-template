# Deployment Notes

## existing project
# Deployment Notes

Deployments require proper setup of git remotes and a working development environment in order to compile production CSS and JS files and push these files to the right servers.

### Local Dev Environment Setup quick guide
- clone repo with this command:
```
git clone git@github.com:xxxxxxx
```

- Follow steps in [GETTING_DJANGO_STARTED.md](GETTING_DJANGO_STARTED.md) to setup vagrant with the necessary Django libs

### Standard deployment work flow
- Deploying to Heroku environments requires that changes first be commited to the corresponding environment branch

- In order to keep the git branches in a clean, conflict free state,  changes should be commited in each branch in ascending order
  - dev
  - staging
  - master (production branch)

- Once changes have been pushed to the corresponding Github branch the Heroku environment can be deployed with the following command (depending on environment):
```
fab dev.deploy
```
or
```
fab staging.deploy
```
or
```
fab production.deploy
```
#### Deploy command notes
- this command will automatically quit the dev server when called.  The dev server may be resterted by re-running `fab runall` command.

- The deploy command: 
  - compiles the js and css files for the corresponding environment
  - uploads these files to the static file store on Amazon S3
  - pushes the updated app to Heroku
  - does any necessary updates to the Heroku Database and Asset version environment variables

-----

Project specific instructions would be included in this file as well.

-----
## New Project

### Heroku quick start
- install the heroku app, if not already installed
- add all of the resources and commit to your git repo.  
- Then create the heroku app, 
- setup the APP_ENV to heroku to use the heroku.py settings file, alternativly this file could be copied to production.py and APP_ENV=production etc.
- create a dev db (or provision a larger db as necessary
- promote db to be default
- deploy to heroku
- syncdb (this step will require creation of an admin user)
- page should serve



```
git add .
git commit -a -m 'initial commit'
heroku create app-name
heroku config:set APP_ENV=dev # or staging or production depending on which env you are working on.
heroku addons:add heroku-postgresql:dev
heroku pg:promote HEROKU_POSTGRESQL_(use result from last command)
git push heroku master
heroku run ./manage.py syncdb
heroku open
```


### disable collectstatic on heroku, it does not work with require compile anyway
```
$ heroku config:set DISABLE_COLLECTSTATIC=1
```

### setup app_info.json
Each heroku environment must have a corresponding entry in app_info.json.  This config file is responsible for defining the heroku app name, corresponding app_env name and git remote name.  haus-start will fill in some of these values for you.

```
{
	"dev": {
		"heroku_app_name": "'__PROJECT_SHORT_NAME__-dev",
		"APP_ENV": "dev",
		"heroku_remote_name": "dev",
		"branch_name": "dev",
		"s3_bucket": "__BUCKET_NAME__-dev"
	},
	"staging": {
		"heroku_app_name": "'__PROJECT_SHORT_NAME__-staging",
		"APP_ENV": "staging",
		"heroku_remote_name": "staging",
		"branch_name": "staging",
        	"s3_bucket": "__BUCKET_NAME__-staging"
	},
	"production": {
		"heroku_app_name": "'__PROJECT_SHORT_NAME__",
		"APP_ENV": "production",
		"heroku_remote_name": "production",
		"branch_name": "master",
        	"s3_bucket": "__BUCKET_NAME__"
	}
}```

