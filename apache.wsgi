# used for mod_wsgi
import sys
sys.path.insert(0, '/var/www/monitornjus') # change path!
from app import app as application