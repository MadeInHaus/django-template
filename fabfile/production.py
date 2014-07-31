from heroku import CustomTask, deploy, deploy_source, deploy_static_media,\
    deploy_user_media, sync_prod_db, create_fixture_on_s3, grab_fixture_on_s3,\
    apply_fixture

deploy = CustomTask(deploy, 'production', quick=False)
deploy_source = CustomTask(deploy_source, 'production')
deploy_static_media = CustomTask(deploy_static_media, 'production')
deploy_user_media = CustomTask(deploy_user_media, 'production')
sync_prod_db = CustomTask(sync_prod_db, 'production')
create_fixture_on_s3 = CustomTask(create_fixture_on_s3, 'production')
grab_fixture_on_s3 = CustomTask(grab_fixture_on_s3, 'production')
apply_fixture = CustomTask(apply_fixture, 'production')

