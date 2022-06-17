"""AdomanyOldal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ast import pattern
from xml.etree.ElementInclude import include
from django import views
from django.contrib import admin
from django.urls import path, include
# kiegészítés
from app import views

urlpatterns = [
    path('', views.kezdolap, name='home'),
    path('kezdolap/', views.kezdolap, name="kezdolap"),
    path('rolunk/', views.rolunk, name="rolunk"),
    path('regisztral/', views.regisztral, name="regisztral"),
    path("bejelentkez/", views.bejelentkezes, name="bejelentkezes"),
    path("profil/", views.profil, name="profil"),
    path("szerk", views.profilSzerk, name="profilSzerk"),
    path("egyenlegFel", views.egyenlegFel, name="egyenlegFel"),
    path("ujGyujtes", views.ujGyujtes, name="ujGyujtes"),
    path("gyujtes/<int:gyujtesID>/<string:sikeres>/", views.gyujtesReszlet, name="gyujtes"),
    path("gyujtesStat/", views.gyujtesStat, name="gyujtesStat"),
    path("kijelentkezes/", views.logout_request, name="kijelentkezes"),
    path('admin/', admin.site.urls),

]
