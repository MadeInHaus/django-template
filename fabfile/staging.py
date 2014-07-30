from heroku import CustomTask, deploy, deploy_source, deploy_static_media, deploy_user_media, sync_prod_db

deploy = CustomTask(deploy, 'staging', quick=True )
deploy_source = CustomTask(deploy_source, 'staging', quick=True )
deploy_static_media = CustomTask(deploy_static_media, 'staging', quick=True )
deploy_user_media = CustomTask(deploy_user_media, 'staging', quick=True )
sync_prod_db = CustomTask(sync_prod_db, 'staging', quick=True )
