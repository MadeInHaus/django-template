# Run python manage.py reset_db to start from afresh then do a sync.
# Original code by dnordberg at http://djangosnippets.org/snippets/828/

from django.conf import settings
from django.core.management.base import CommandError
import logging
from django.core.management.base import BaseCommand
from django.db import connection
        
class Command(BaseCommand):
    help = "Resets a database."

    def handle(self, *args, **options):
        """
        Resets a database.
        """
        database = settings.DATABASES['default']
        if 'sqlite3' in database['ENGINE']:
            import os
            try:
                logging.info("Unlinking sqlite3 database")
                os.unlink(database['NAME'])
            except OSError:
                pass
        elif 'mysql' in database['ENGINE']:
            import MySQLdb as Database
            kwargs = {
                'user': database['USER'],
                'passwd': database['PASSWORD'],
            }
            if database['HOST'].startswith('/'):
                kwargs['unix_socket'] = database['HOST']
            else:
                kwargs['host'] = database['HOST']
            if database['PORT']:
                kwargs['port'] = int(database['PORT'])
            connection = Database.connect(**kwargs)
            drop_query = 'DROP DATABASE IF EXISTS %s' % database['NAME']
            create_query = 'CREATE DATABASE %s' % database['NAME']
            logging.info('Executing... "' + drop_query + '"')
            connection.query(drop_query)
            logging.info('Executing... "' + create_query + '"')
            connection.query(create_query)
        elif 'postgresql' in database['ENGINE']:
            if 'postgresql_psycopg2' in database['ENGINE']:
                import psycopg2 as Database
            else:
                import psycopg as Database
    
            if database['NAME'] == '':
                from django.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured, "You need to specify DATABASE_NAME in your Django settings file."
            if database['USER']:
                conn_string = "user=%s" % (database['USER'])
            if database['PASSWORD']:
                conn_string += " password='%s'" % database['PASSWORD']
            if database['HOST']:
                conn_string += " host=%s" % database['HOST']
            if database['PORT']:
                conn_string += " port=%s" % database['PORT']
            connection = Database.connect(conn_string)
            connection.set_isolation_level(0) #autocommit false
            cursor = connection.cursor()
            drop_query = 'DROP DATABASE %s' % database['NAME']
            logging.info('Executing... "' + drop_query + '"')
    
            try:
                cursor.execute(drop_query)
            except Database.ProgrammingError, e:
                logging.info("Error: "+str(e))
    
            # Encoding should be SQL_ASCII (7-bit postgres default) or prefered UTF8 (8-bit)
            create_query = ("""
CREATE DATABASE %s
    WITH OWNER = %s
        ENCODING = 'UTF8'
        TABLESPACE = pg_default;
""" % (database['NAME'], database['USER']))
            logging.info('Executing... "' + create_query + '"')
            cursor.execute(create_query)
    
        else:
            raise CommandError, "Unknown database engine %s" % database['ENGINE']
    
        logging.info("Reset success")
