include:
  - sql.postgres

vagrant.postgres.createsuperuser:
  postgres_database.present:
    - name: django

vagrant.postgres.user:
 postgres_user.present:
   - superuser: True
   - name: vagrant
   - require: 
     - pkg: postgresql-server