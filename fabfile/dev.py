from heroku import CustomTask, deploy, deploy_source, deploy_static_media,\
    deploy_user_media, sync_prod_db, create_fixture_on_s3, grab_fixture_on_s3,\
    apply_fixture

deploy = CustomTask(deploy, 'dev')
deploy_source = CustomTask(deploy_source, 'dev')
deploy_static_media = CustomTask(deploy_static_media, 'dev')
deploy_user_media = CustomTask(deploy_user_media, 'dev')
sync_prod_db = CustomTask(sync_prod_db, 'dev')
create_fixture_on_s3 = CustomTask(create_fixture_on_s3, 'dev')
grab_fixture_on_s3 = CustomTask(grab_fixture_on_s3, 'dev')
apply_fixture = CustomTask(apply_fixture, 'dev')

