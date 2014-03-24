from heroku import CustomTask, deploy, deploy_source, deploy_static_media, deploy_user_media, sync_prod_db

deploy = CustomTask(deploy, 'production')
deploy_source = CustomTask(deploy_source, 'production')
deploy_static_media = CustomTask(deploy_static_media, 'production')
deploy_user_media = CustomTask(deploy_user_media, 'production')
sync_prod_db = CustomTask(sync_prod_db, 'production')
