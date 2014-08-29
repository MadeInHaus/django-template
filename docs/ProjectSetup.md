

- create heroku apps
  - db
  - dbbackups
  - newrelic
  - set env vars (heroku config:set)
    - APP_ENV:                     production
    - DISABLE_COLLECTSTATIC:       1
    - USE_RELATIVE_STATIC_URL:     1 (if serving through cloudfront)
