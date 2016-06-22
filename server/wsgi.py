import os
env = os.environ.get("DIVVY_ENV", None)
if env:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.%s" % os.environ["DIVVY_ENV"])
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

