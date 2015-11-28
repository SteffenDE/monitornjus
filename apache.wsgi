# used for mod_wsgi
import sys
sys.path.insert(0, '/var/www/monitornjus') # change path!
from monitornjus import app as application