from django.urls import path
from khateeb_site.views import home, translate_text, transcribe_audio
urlpatterns=[
    path("",home,name="home"),
    path("api/translate/",translate_text,name="translate_text"),
    path("api/transcribe/",transcribe_audio,name="transcribe_audio"),
]
