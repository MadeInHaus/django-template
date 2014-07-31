from heroku import CustomTask, deploy, deploy_source, deploy_static_media,\
    deploy_user_media, sync_prod_db, create_fixture_on_s3, grab_fixture_on_s3,\
    apply_fixture

deploy = CustomTask(deploy, 'staging')
deploy_source = CustomTask(deploy_source, 'staging')
deploy_static_media = CustomTask(deploy_static_media, 'staging')
deploy_user_media = CustomTask(deploy_user_media, 'staging')
sync_prod_db = CustomTask(sync_prod_db, 'staging')
create_fixture_on_s3 = CustomTask(create_fixture_on_s3, 'staging')
grab_fixture_on_s3 = CustomTask(grab_fixture_on_s3, 'staging')
apply_fixture = CustomTask(apply_fixture, 'staging')

