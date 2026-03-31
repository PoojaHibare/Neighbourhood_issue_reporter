import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neighborhood_issue_reporter.settings')
application = get_wsgi_application()
