from heroku import CustomTask, deploy, deploy_source, deploy_static_media, deploy_user_media, sync_prod_db

deploy = CustomTask(deploy, quick=True, 'dev')
deploy_source = CustomTask(deploy_source, quick=True, 'dev')
deploy_static_media = CustomTask(deploy_static_media, quick=True, 'dev')
deploy_user_media = CustomTask(deploy_user_media, quick=True, 'dev')
sync_prod_db = CustomTask(sync_prod_db, quick=True, 'dev')
