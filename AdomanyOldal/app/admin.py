from django.contrib import admin
from .models import felhasznalo, gyujtes, fizetes

# Register your models here.


class felhasznaloAdmin(admin.ModelAdmin):
    fields = ["becenev", "egyenleg"]


class gyujtesAdmin(admin.ModelAdmin):
    fields = ["publikalo", "cim", "leiras",
              "promocios", "minAr", "cel", "jelenleg", "datumIdo_UTC", "celDatum"]


class fizetesAdmin(admin.ModelAdmin):
    fields = ["ki", "gyujtesnek", "mennyit", "megjegyzes", "datumIdo_UTC"]


admin.site.register(felhasznalo, felhasznaloAdmin)
admin.site.register(gyujtes, gyujtesAdmin)
admin.site.register(fizetes, fizetesAdmin)
