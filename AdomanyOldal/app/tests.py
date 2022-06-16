from ast import Try
import email
from django.test import TestCase
from more_itertools import last
from pyparsing import null_debug_action
#from requests import request
from django.http import HttpRequest
from requests import request
from .models import felhasznalo
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.models import gyujtes
# Create your tests here.

class ProfilTeszt01_first_name_Eleres(TestCase):
    def setUp(self):
        User.objects.create(username="teszt1", first_name="Asd",
                            last_name="QWERTZ", email="ASD@QWERTZ.com")

    def test(self):
        try:
            print()
            szemelyKeres = User.objects.get(username="teszt1")
            print(szemelyKeres)
            szemelyKeres_first_name = szemelyKeres.first_name
            print(szemelyKeres_first_name)
        except User.DoesNotExist:
            print("Személy keresése....")
            for i in User:
                print(i)

        print("név frissítés")
        nev = "Yuumi"
        szemelyKeres = User.objects.get(username="teszt1")
        szemelyKeres.first_name = nev
        szemelyUjNev = szemelyKeres.first_name
        print(szemelyUjNev)

class GyujtesTeszt01(TestCase):
    def setUp(self):
        User.objects.create(username="teszt1", first_name="Asd", last_name="QWERTZ", email="ASD@QWERTZ.com", id=99)
    def test(self):
        try:
            tesztGyujtes= gyujtes.objects.create(publikalo_id=99, cim="proba", leiras="qwertz", promocios=0,
                                                 minAr=10, cel=100 )
            print(tesztGyujtes)
            for i in gyujtes:
                print(i)
        except gyujtes.DoesNotExist:
            print("A gyüjtes nem jött létre")