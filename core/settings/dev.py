from .common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7w-9t(jvb_=1#6c&sa6**jf%bvur2pg7+pqr_04ri!!cq@$=j4"

ALLOWED_HOSTS = []

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        # 'silk.middleware.SilkyMiddleware',
    ]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.sqlite3",
        # "NAME": BASE_DIR / "db.sqlite3",
        "ENGINE": "django.db.backends.mysql",
        "NAME": "storefront3",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "hp15CC154TX",
    }
}
