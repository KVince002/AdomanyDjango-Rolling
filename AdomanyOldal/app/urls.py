from django.urls import URLPattern, path
from django.conf.urls import url
from . import views

app_name = "app"

urlpatterns = [
    path("", views.kezdolap, name="kezdolap"),
    url(r"^?P<gyujtesID>/$", views.gyujtesReszlet, name="gyujtesReszlet")
]
