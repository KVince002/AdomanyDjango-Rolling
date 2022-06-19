from dataclasses import fields
import email
from pickle import FALSE
from pyexpat import model
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.db import models
from django.forms import ModelForm
from django.http import HttpRequest
#from requests import request
#from requests import request
# from django.core import MinValueValidator
from app.models import felhasznalo, gyujtes


class Regisztralas(UserCreationForm):
    username = forms.CharField(
        label="Felhasználónév", min_length=3, max_length=150)
    # first_name = forms.CharField(label="Előnév")
    # last_name = forms.CharField(label="Utónév")
    email = forms.EmailField(label="Email cím")
    password1 = forms.CharField(label="Jelszava", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Jelszava még egyszer", widget=forms.PasswordInput)

    def clean_felhasznalo(self):
        username = self.cleaned_data['username'].lower()
        keres = User.objects.filter(username=username)
        if keres.count():
            raise ValidationError("Ez a felhasználónév már létezik!")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        keres = User.objects.filter(email=email)
        if keres.count():
            raise ValidationError("Ez az email már létezik!")
        return email

    def clean_firstname(self):
        first_name = self.cleaned_data["first_name"].lower()
        return first_name

    def clean_lastname(self):
        last_name = self.cleaned_data["last_name"].lower()
        return last_name
    # ezzel lehet ellenőrizni hogy a két jelszó mező egyezik-e

    def clean_jelszomegint(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("A jelszavak nem egyeznek!")
        return password2

    def mentes(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data["email"],
            #! ezek szerint nem így kell hozzáadni
            # self.cleaned_data["first_name"],
            # self.cleaned_data["last_name"],
            self.cleaned_data["password2"],
        )
        return user


class felhasznaloFrissitForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
    first_name = forms.CharField(label="Előnév", required=False)
    last_name = forms.CharField(label="Utónév", required=False)
    email = forms.EmailField(label="Email cím", required=False)
    password1 = forms.CharField(
        label="Jelszava", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(
        label="Jelszava még egyszer", widget=forms.PasswordInput, required=False)

    def __str__(self) -> str:
        return super().__str__()

    # def mentes(self, commit=True):
    #     user = User.objects.get(id=request.user.id).update(
    #         self.cleaned_data.get["email"],
    #         self.cleaned_data.get["first_name"],
    #         self.cleaned_data.get["last_name"],
    #         self.cleaned_data.get["password2"],
    #     )
    #     return user

# gyűjtés model form


class gyujtesForm(ModelForm):
    class Meta:
        model = gyujtes
        fields = ["cim", "leiras", "promocios", "minAr", "cel"]

    cim = forms.CharField(label="Cim")
    leiras = forms.CharField(widget=forms.Textarea,
                             label="Adjon meg egy részletes leírást")
    promocios = forms.BooleanField(
        label="Promótálja-e?", required=False, help_text="Ez az összeg a 0,25x-orosa amegadott célnak!")
    minAr = forms.IntegerField(
        label="Adjon meg hogy mennyit lehet minimum adományozni", min_value=1)
    cel = forms.IntegerField(
        label="Mennyit szeretne elérni a gyűjtésével?", min_value=1)

    def __str__(self) -> str:
        return super().__str__()

# bankkártya form


class bankkartya(forms.Form):
    szam = forms.CharField(max_length=16, required=True, label="Kártya száma")
    tulaj = forms.CharField(required=True, label="Kártya birtokos")
    lejarat = forms.CharField(
        required=True, label="Lejárat (csak a négyszám elválasztás nélkül)", max_length=4)
    cvkod = forms.CharField(
        required=True, label="Biztonsági szám", max_length=3)
    osszeg = forms.IntegerField(required=True)

# pénz adományozás


class fizetesForm(forms.Form):
    osszeg = forms.IntegerField(required=True)
    megjegyzes = forms.CharField(required=False, max_length=254)
