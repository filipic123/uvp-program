import bottle
from datetime import date
from model import Stanje, Fransiza, Oseba

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
        stanje = Stanje.iz_datoteke(ime_datoteke)
    except FileNotFoundError:
        stanje = Stanje.iz_datoteke("stanje.json")
        stanje.v_datoteko(ime_datoteke)
    return stanje

def shrani_stanje_trenutnega_uporabnika(stanje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SIFRIRNI_KLJUC)
    ime_datoteke = ime_uporabnikove_datoteke(uporabnisko_ime)
    stanje.v_datoteko(ime_datoteke)

def url_fransize(id_fransize):
    return f"/fransiza/{id_fransize}/"


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template(
        "prijava.html"
    )

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if uporabnisko_ime == geslo:
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
        "zacetna_stran.html",
        fransize=stanje.fransize,
    )

@bottle.get("/fransiza/<id_fransize:int>/")
def prikazi_fansizo(id_fransize):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    return bottle.template(
        "fransiza.tpl",
        fransiza=stanje.fransize,
        aktualna_fransiza=fransiza,
        id_aktualne_fransize=id_fransize,
    )


@bottle.get("/dodaj-fansizo/")
def dodaj_fransizo_get():
    return bottle.template(
        "dodaj_fransizo.tpl", napake={}, polja={}
    )


@bottle.post("/dodaj-fansizo/")
def dodaj_fransizo_post():
    stanje = stanje_trenutnega_uporabnika()
    ime = bottle.request.forms.getunicode("ime")
    fransiza = Fransiza(ime, osebe=[])
    napake = stanje.preveri_podatke_nove_fransize(fransiza)
    if napake:
        polja = {"ime": ime}
        return bottle.template("dodaj_fransizo.tpl", napake=napake, polja=polja)
    else:
        id_fransize = stanje.dodaj_fransizo(fransiza)
        shrani_stanje_trenutnega_uporabnika(stanje)
        bottle.redirect(url_fransize(id_fransize))


@bottle.post("/opravi/<id_fransize:int>/<id_opravila:int>/")
def opravi(id_fransize, id_opravila):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    oseba = fransiza.opravila[id_opravila]
    oseba.opravi()
    shrani_stanje_trenutnega_uporabnika(stanje)
    bottle.redirect(url_fransize(id_fransize))

@bottle.post("/dodaj-oseba/<id_fransize:int>/")
def dodaj_osebo(id_fransize):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    opis = bottle.request.forms.getunicode("opis")
    if bottle.request.forms["rok"]:
        rok = date.fromisoformat(bottle.request.forms["rok"])
    else:
        rok = None
    oseba = oseba(opis, rok)
    fransiza.dodaj_osebo(oseba)
    shrani_stanje_trenutnega_uporabnika(stanje)
    bottle.redirect(url_fransize(id_fransize))


@bottle.error(404)
def error_404():
    return "Ta stran ne obstaja!"


bottle.run(debug=True, reloader=True)