from django.contrib import admin
from .models import felhasznalo, gyujtes, fizetes

# Register your models here.


class felhasznaloAdmin(admin.ModelAdmin):
    fields = ["becenev", "telefon", "egyenleg"]


class gyujtesAdmin(admin.ModelAdmin):
    fields = ["publikalo", "cim", "leiras",
              "promocios", "minAr", "cel", "jelenleg"]


class fizetesAdmin(admin.ModelAdmin):
    fields = ["ki", "gyujtesnek", "mennyit", "megjegyzes"]


admin.site.register(felhasznalo, felhasznaloAdmin)
admin.site.register(gyujtes, gyujtesAdmin)
admin.site.register(fizetes, fizetesAdmin)
