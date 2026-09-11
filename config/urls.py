from django.urls import path
from khateeb_site.views import home, translate_text, translate_hadith

urlpatterns=[
    path("",home,name="home"),
    path("api/translate/",translate_text,name="translate_text"),
    path("api/hadith/",translate_hadith,name="translate_hadith"),
]
