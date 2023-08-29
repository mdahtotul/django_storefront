import os
import dj_database_url
from decouple import config
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ['vercel.app', 'now.sh']

DATABASES = {
    "default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))
}
