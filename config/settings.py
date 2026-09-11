import os
from pathlib import Path
import dj_database_url
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv("SECRET_KEY","dev-only-change-me")
DEBUG=os.getenv("DEBUG","True").lower()=="true"
ALLOWED_HOSTS=["*"]
INSTALLED_APPS=["django.contrib.contenttypes","django.contrib.staticfiles","khateeb_site"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","django.middleware.common.CommonMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"khateeb_site"/"templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":[]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default": dj_database_url.config(default=f"sqlite:///{BASE_DIR/'db.sqlite3'}", conn_max_age=600)}
LANGUAGE_CODE="ar"
TIME_ZONE="Asia/Riyadh"
USE_I18N=True
USE_TZ=True
STATIC_URL="/static/"
STATIC_ROOT=BASE_DIR/"staticfiles"
STATICFILES_DIRS=[BASE_DIR/"khateeb_site"/"static"]
STORAGES={"staticfiles":{"BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage"}}
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
ARGOS_MODEL_DIR=os.getenv("ARGOS_MODEL_DIR",".argos")
