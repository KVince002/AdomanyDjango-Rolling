from ast import If
import email
from pyexpat.errors import messages
from re import template
from urllib.request import Request
import django
from django.shortcuts import render, redirect
from django.http import HttpRequest
# W3Schools szerint
from django.template import loader
# regisztálás form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
# saját regisztrációs form
from django.contrib import messages
from django.contrib.auth.models import User
# későbbre
from django.contrib.auth.decorators import login_required
# saját bejelentkezésre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# from more_itertools import first
# profil szerkeztéshez
from app.forms import Regisztralas, bankkartya, felhasznaloFrissitForm, gyujtesForm
from app.models import felhasznalo, fizetes, gyujtes
# fizetéshez
from app.forms import fizetesForm

# Create your views here.


def kezdolap(request):

    # VS22 djangoWEB projekt szerint
    assert isinstance(request, HttpRequest)
    # gyujtesek model átadása és szortírozása
    promos = []
    atlagos = []
    user = request.user
    for i in gyujtes.objects.all():
        if i.promocios == True:
            promos.append(i)
        else:
            atlagos.append(i)
    return render(request, "templates/app/home.html", {"cim": "Adok neki! - Adomány oldal", "atlagos": atlagos,
                                                       "promos": promos, "user": user})


def rolunk(request):
    assert isinstance(request, HttpRequest)
    return render(request, "templates/app/about.html", {"cim": "Adok neki! - Rólunk"})


def regisztral(request):
    if request.method == "POST":
        regUrlap = Regisztralas(request.POST)
        # ellenőrzés
        if regUrlap.is_valid():
            regisztraltFelhasznalo = regUrlap.mentes()
            messages.success(request, "Fiok sikeresen letrehozva")
            # bejelentkezteti
            login(request, regisztraltFelhasznalo)
            # felhasznalo modell előkészítése
            if User.objects.filter(id=request.user.id):
                regisztraltFelhasznalo_Id = User.objects.get(
                    id=request.user.id)
            # adatok feltöltése a modelbe
            felhasznaloModel = felhasznalo(
                becenev=regisztraltFelhasznalo_Id, egyenleg=0)
            felhasznaloModel.save()

            # tovább küldi
            return redirect("profil")  # * továbbítás a profilra
    else:
        regUrlap = Regisztralas()
    return render(request, "templates/app/signUp.html", {"cim": "Adok neki! - Regisztrálás", "form": regUrlap})


def bejelentkezes(request):
    beUrlap = AuthenticationForm()
    if request.method == "POST":
        beUrlap = AuthenticationForm(request, data=request.POST)
        if beUrlap.is_valid():
            # adatok ellenőrzése
            felhasznalonev = beUrlap.cleaned_data.get("username")
            jelszo = beUrlap.cleaned_data.get("password")
            # ezzel ellenőrizzük, hogy a megadott felhasználónév és a jelszó, jó-e
            felhasznalo = authenticate(
                username=felhasznalonev, password=jelszo)
            # felhasználó létezik-e?
            if felhasznalo is not None:
                login(request, felhasznalo)
                # továbbítás
                return redirect("profil")
            else:
                messages.error(
                    request, F"Sikertelen bejelentkezés, előfordulhat, hogy rossz a jelszót adhatott meg!")
    beUrlap = AuthenticationForm()
    return render(request, "templates/app/signIn.html", context={"cim": "Adok neki! - Bejelentkezés", "form": beUrlap})


def profil(request):
    assert isinstance(request, HttpRequest)
    felhasznaloAlapertelmezett = User.objects.get(id=request.user.id)
    felhasznaloKiegeszito = felhasznalo.objects.get(becenev=request.user.id)
    return render(request, "templates/app/profil.html", {"cim": "Adok neki! - Profil", "felhasznaloAlapertelmezett": felhasznaloAlapertelmezett, "felhasznaloKiegeszito": felhasznaloKiegeszito})

# kijelentkezés


def logout_request(request):
    logout(request)
    # üzenet ha szeretnék
    return redirect("kezdolap")

# profil szerkeztés


def profilSzerk(request):
    if request.method == "POST":
        frissitform = felhasznaloFrissitForm(request.POST)
        if frissitform.is_valid():
            emailCim = frissitform.cleaned_data["email"]
            elonev = frissitform.cleaned_data["first_name"]
            utonev = frissitform.cleaned_data["last_name"]
            jelszo = frissitform.cleaned_data["password2"]
            # meglévő adatok
            UserMeglevo = User.objects.get(id=request.user.id)
            # érték ellenőrzés
            if emailCim == "":
                emailCim = UserMeglevo.email
            if elonev == "":
                elonev = UserMeglevo.first_name
            if utonev == "":
                utonev = UserMeglevo.last_name
            if jelszo == "":
                jelszo = UserMeglevo.password
            # mentés a modelba
            UserMentes = User.objects.get(username=request.user.username)
            UserMentes.email = emailCim
            UserMentes.first_name = elonev
            UserMentes.last_name = utonev
            UserMentes.password = jelszo
            UserMentes.save()
            print(UserMentes)
    else:
        frissitform = felhasznaloFrissitForm(request.POST)
    return render(request, "templates/app/profilSzerk.html", {"cim": "Adok neki! - Profil szerkesztés", "form": frissitform})


def egyenlegFel(request):
    if request.method == "POST":
        feltoltes = bankkartya(request.POST)
        if feltoltes.is_valid():
            egyenlegHozzaAd = feltoltes.cleaned_data["osszeg"]
            felhasznaloJelenleg = felhasznalo.objects.get(
                becenev=request.user.id)
            egyenlegJelenleg = felhasznaloJelenleg.egyenleg
            egyenlegUj = egyenlegJelenleg+egyenlegHozzaAd
            # model frissítése
            felhasznaloFrissit = felhasznalo.objects.filter(
                becenev=request.user.id).update(egyenleg=egyenlegUj)
            # mentés
            egyenlegModositott = felhasznalo.objects.get(
                becenev=request.user.id)
            if egyenlegModositott.egyenleg > egyenlegJelenleg:
                return redirect("profil")
    else:
        feltoltes = bankkartya(request.POST)
    return render(request, "templates/app/egyenlegFel.html", {"cim": "Adok neki! - Egyenleg feltöltés", "form": feltoltes})


def ujGyujtes(request):
    # kezdeményező felhasználó adatainak lekérése
    AlapUserModel = User.objects.get(id=request.user.id)
    felhasznaloModel = felhasznalo.objects.get(becenev=AlapUserModel.id)
    # form működésre bírása
    if request.method == "POST":
        UjGyujtes = gyujtesForm(request.POST)
        if UjGyujtes.is_valid():
            cim = UjGyujtes.cleaned_data["cim"]
            leiras = UjGyujtes.cleaned_data["leiras"]
            promocio = UjGyujtes.cleaned_data["promocios"]
            minAr = UjGyujtes.cleaned_data["minAr"]
            cel = UjGyujtes.cleaned_data["cel"]
            # dictionry létrehozása, tárolásra
            AdatokDic = {"Cim": cim, "Leiras": leiras,
                         "Promo": promocio, "MinAr": minAr, "Cel": cel}
            # ha nincs elég egyenlege akkor ne lehessen promóciós gyűjtést létrehozni
            if AdatokDic.get("Promo") >= felhasznaloModel.egyenleg:
                # promocios ár levonása
                felhasznaloModel.egyenleg-200
                felhasznaloModel.save()
                # mentés
                UjGyujtesSeged = UjGyujtes.save(commit=False)
                UjGyujtesSeged.publikalo = request.user
                UjGyujtesSeged.save()
            else:
                UjGyujtesSeged = gyujtes.objects.create(publikalo=User.objects.get(id=request.user.id), cim=AdatokDic.get(
                    "Cim"), leiras=AdatokDic.get("Leiras"), promocios=False, minAr=AdatokDic.get("MinAr"), cel=AdatokDic.get("Cel"))
                UjGyujtesSeged.save()

            # átirányítás
            return redirect("profil")
    else:
        UjGyujtes = gyujtesForm(request.POST)
    FelhasznaloAlapertelmezett = request.user
    return render(request, "templates/app/ujGyujtes.html", {"cim": "Adok neki! - Egyenleg feltöltés", "form": UjGyujtes, "FelhasznaloAlapertelmezett": FelhasznaloAlapertelmezett})


def gyujtesStat(request):

    FelhasznaloAlapertelmezett = request.user
    return render(request, "templates/app/gyujtesStat.html", {"cim": "Adok neki! - Egyenleg feltöltés", "FelhasznaloAlapertelmezett": FelhasznaloAlapertelmezett})


def gyujtesReszlet(request, gyujtesID):
    print(f"gyujtesReszlet pramétere: {gyujtesID}")
    gyujtesID = gyujtesID
    print(f"gyujtesReszlet paramétere utólag: {gyujtesID}")
    gyujtesReszletek = gyujtes.objects.get(id=gyujtesID)

    # fizetes form működésre bírása
    if request.method == "POST":
        fizetesElbiralasa = fizetesForm(request.POST)
        if fizetesElbiralasa.is_valid():
            # form elemek mentése
            fizetendo = fizetesElbiralasa.cleaned_data["osszeg"]
            print(fizetendo)
            megjegyzes = fizetesElbiralasa.cleaned_data["megjegyzes"]
            print(megjegyzes)
            # szükséges adatok ellenőrzése a vásárláshoz
            sikeresFizetes= False
            adomanyozoFelh = felhasznalo.objects.get(becenev=request.user.id)
            if adomanyozoFelh.egyenleg >= fizetendo:
            # státusz
                sikeresFizetes = True
                print(sikeresFizetes)
            # fizetés végrehajtása
                adomanyozoFelh.egyenleg -= fizetendo
                gyujtesTargy = gyujtes.objects.get(id=gyujtesID)
                gyujtesTargy.jelenleg += fizetendo
                adomanyGyujto = felhasznalo.objects.get(becenev=gyujtesTargy.publikalo_id)
                adomanyGyujto.egyenleg += fizetendo
                #használt modellek mentése
                gyujtesTargy.save()
                adomanyozoFelh.save()
                adomanyGyujto.save()
                # fizetés mentése modellba
                fizetesMentes = fizetes.objects.create(ki=adomanyozoFelh.becenev, gyujtesnek=gyujtes.objects.get(id=gyujtesID), mennyit=fizetendo, megjegyzes=megjegyzes)
                fizetesMentes.save()
            #ha nem sikerül
            #TODO else rész befejezése
            else:
                sikeresFizetes = False
                print(sikeresFizetes)
    else:
        fizetesElbiralasa = fizetesForm(request.POST)
    return render(request, "templates/app/gyujtesReszlet.html", {"cim": "Adok neki! - "+gyujtesReszletek.cim, "gyujtesReszletek": gyujtesReszletek, "form": fizetesElbiralasa, "sikeresFizetes":sikeresFizetes})


def gyujtesStat(request):
    # segéd
    UserModel = User.objects.get(id=request.user.id)
    # fizetés ellenőrzés
    fizetesek = fizetes.objects.filter(ki=UserModel.id)
    print("eltárolt fizetések")
    for i in fizetesek:
        print(i.id)
    print("fizetesek ==0?")
    if len(fizetesek) == 0:
        print("aha")
        fizetesek = "Ön még nem adományozott semmilyen célnak eddig."
    else:
        print("ha nem")
        print(len(fizetesek))
    # gyüjtés ellenőrzés
    gyujtesek = gyujtes.objects.filter(publikalo=UserModel.id)
    print("eltárolt gyüjtések")
    for i in gyujtesek:
        print(i.id)
    print("gyujtesek ==0?")
    if len(gyujtesek) == 0:
        print("aha")
        gyujtesek = "Ön még nem hozott létre egy gyűjtést sem."
    else:
        print("ha nem")
        print(gyujtesek)
        print(len(gyujtesek))
    return render(request, "templates/app/gyujtesStatisztika.html", {"cim": "Adok neki! - Gyűjtés és fizetés statisztikák", "fizetesek": fizetesek, "gyujtesek": gyujtesek})
