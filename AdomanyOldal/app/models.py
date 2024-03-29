from pyexpat import model
from time import timezone
import zoneinfo
from django.conf import settings
from django.db import models
from django.forms import CharField
from datetime import date, datetime, time
from django.utils import timezone
# from requests import request

# Create your models here.


class felhasznalo(models.Model):
    # ? jobbesetben megkapja
    becenev = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    egyenleg = models.IntegerField(default=0)

    class Meta:
        ordering = ["id"]
    # ? szép kiegészítés

    def __str__(self) -> str:
        return super().__str__()


class gyujtes(models.Model):
    publikalo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cim = models.CharField(max_length=255)
    leiras = models.TextField()
    # ezen a néven fog megjelenni, ugyan nem kötöm össze a User táblával
    promocios = models.BooleanField(default=False)
    minAr = models.IntegerField(null=False)
    cel = models.IntegerField()
    # utólagos kiegészítés
    jelenleg = models.IntegerField(default=0)
    # dátum és idő hozzáadása
    datumIdo_UTC = models.DateTimeField(default=timezone.now())
    # cel datum és idő hozzáadása
    celDatum = models.DateTimeField(null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return super().__str__()

# még csak teszt gondolat
# 2:30 de már benne is lesz


class fizetes(models.Model):
    ki = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gyujtesnek = models.ForeignKey(gyujtes, on_delete=models.CASCADE)
    mennyit = models.IntegerField()
    megjegyzes = models.CharField(null=True, max_length=255)
    # dátum és idő
    datumIdo_UTC = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return super().__str__()


class visszautalas(models.Model):
    ki = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mennyit = models.IntegerField()
    datumIdo_UTC = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return super().__str__()
