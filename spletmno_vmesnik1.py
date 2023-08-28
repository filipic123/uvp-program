import bottle
from datetime import date
from model1 import Stanje, Fransiza, Oseba

SIFRIRNI_KLJUC = "To je poseben šifrirni ključ"

def ime_uporabnikove_datoteke(uporabnisko_ime):
    return f"stanja_uporabnikov/{uporabnisko_ime}.json"


def stanje_trenutnega_uporabnika():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SIFRIRNI_KLJUC)
    if uporabnisko_ime == None:
        bottle.redirect("/prijava/")
    else:
        uporabnisko_ime = uporabnisko_ime
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    try:
        stanje = Stanje.preberi_iz_datoteke(ime_datoteke)
    except FileNotFoundError:
        stanje = Stanje.preberi_iz_datoteke("primer-stanja.json")
        stanje.shrani_v_datoteko(ime_datoteke)
    return stanje

def shrani_stanje_trenutnega_uporabnika(stanje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SIFRIRNI_KLJUC)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    stanje.shrani_v_datoteko(ime_datoteke)

def url_kategorije(id_kategorije):
    return f"/kategorija/{id_kategorije}/"


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template(
        "prijava.tpl"
    )

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if uporabnisko_ime == geslo[::-1]:
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SIFRIRNI_KLJUC)
        bottle.redirect("/")
    else:
        return "Napaka ob prijavi"

@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    bottle.redirect("/")


@bottle.get("/")
def zacetna_stran():
    stanje = stanje_trenutnega_uporabnika()
    return bottle.template(
        "zacetna_stran.tpl",
        kategorije=stanje.kategorije,
    )