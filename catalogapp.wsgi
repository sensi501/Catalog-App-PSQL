#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Catalog-App-PSQL/")

from CATALOG-APP-PSQL import app as application
application.secret_key = 'Add your secret key'