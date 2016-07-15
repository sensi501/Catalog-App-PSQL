#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Catalog-App-PSQL/")

from __init__ import app as application
<<<<<<< HEAD
application.secret_key = 'Add your secret key'
=======
application.secret_key = 'super_secret_key'
>>>>>>> origin/master
