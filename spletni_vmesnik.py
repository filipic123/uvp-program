import bottle
from model import Stanje, Fransiza, Oseba


SIFRIRNI_KLJUC = "To je poseben šifrirni ključ"


def ime_uporabnikove_datoteke(uporabnisko_ime):
    return f"stanja/{uporabnisko_ime}.json"


def stanje_trenutnega_uporabnika():
    uporabnisko_ime = bottle.request.get_cookie(
        "uporabnisko_ime", secret=SIFRIRNI_KLJUC)
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
    uporabnisko_ime = bottle.request.get_cookie(
        "uporabnisko_ime", secret=SIFRIRNI_KLJUC)
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
    if uporabnisko_ime == geslo and geslo != "":
        bottle.response.set_cookie(
            "uporabnisko_ime",   uporabnisko_ime, path="/", secret=SIFRIRNI_KLJUC)
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
def prikazi_fransizo(id_fransize):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    return bottle.template(
        "fransiza.html",
        fransize=stanje.fransize,
        aktualna_fransiza=fransiza,
        id_aktualne_fransize=id_fransize,
        napaka1=None, napaka2=None, napaka3=None
    )


@bottle.get("/dodaj-fransizo/")
def dodaj_fransizo_get():
    return bottle.template(
        "dodaj_fransizo.html", napake={}, polja={}
    )


@bottle.post("/dodaj-fransizo/")
def dodaj_fransizo_post():
    stanje = stanje_trenutnega_uporabnika()
    lokacija = bottle.request.forms.getunicode("lokacija")
    fransiza = Fransiza(lokacija, osebe=[])
    napake = stanje.preveri_podatke_nove_fransize(fransiza)
    if napake or not lokacija:
        polja = {"lokacija": lokacija}
        return bottle.template("dodaj_fransizo.html", napake=napake, polja=polja)
    else:
        id_fransize = stanje.dodaj_fransizo(fransiza)
        shrani_stanje_trenutnega_uporabnika(stanje)
        bottle.redirect(url_fransize(id_fransize))


@bottle.post("/dodaj-osebo/<id_fransize:int>/")
def dodaj_osebo(id_fransize):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    oseba = bottle.request.forms.getunicode("ime_priimek")
    starost = bottle.request.forms.getunicode("starost")
    delovno_mesto = bottle.request.forms.getunicode("delovno_mesto")
    mesecna_placa = bottle.request.forms.getunicode("mesecna_placa")
    napaka = "vnesiti morate pozitivno število"
    if not delovno_mesto or not oseba or not starost or not mesecna_placa:
        napaka = "zapolnite vsa polja"
        return bottle.template("fransiza.html", fransize=stanje.fransize,
                               aktualna_fransiza=fransiza,
                               id_aktualne_fransize=id_fransize,
                               napaka1=None, napaka2=napaka, napaka3=None)
    if int(starost) < 0:
        return bottle.template("fransiza.html", fransize=stanje.fransize,
                               aktualna_fransiza=fransiza,
                               id_aktualne_fransize=id_fransize,
                               napaka1=napaka, napaka2=None, napaka3=None)
    elif int(mesecna_placa) < 1202:
        napaka = "plača ne biti nižja od minimalne plače (1203 €)"
        return bottle.template("fransiza.html", fransize=stanje.fransize,
                               aktualna_fransiza=fransiza,
                               id_aktualne_fransize=id_fransize,
                               napaka1=None, napaka2=napaka, napaka3=None)
    else:
        oseba1 = Oseba(oseba, starost, delovno_mesto, int(mesecna_placa))
        fransiza.dodaj_osebo(oseba1)
        shrani_stanje_trenutnega_uporabnika(stanje)
        bottle.redirect(url_fransize(id_fransize))


@bottle.post("/spremeni-osebi/<id_fransize:int>/<id_osebe:int>/")
def spremeni_osebo(id_fransize, id_osebe):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    oseba = fransiza.osebe[id_osebe]
    sprememba = bottle.request.forms.getunicode("sprememba")
    kolicina_delovno_mesto = bottle.request.forms.getunicode("kolicina/delovno_mesto")
    if sprememba == "placo":
        try:
            int(kolicina_delovno_mesto)
            if -int(kolicina_delovno_mesto) > oseba.mesecna_placa - 1203:
                napaka = "plača ne more pasti pod minimalno plačo (1203 €)"
                return bottle.template("fransiza.html", fransize=stanje.fransize,
                                       aktualna_fransiza=fransiza,
                                       id_aktualne_fransize=id_fransize,
                                       napaka1=None, napaka2=None, napaka3=napaka)
            else:
                oseba.sprememba_place(kolicina_delovno_mesto)
                shrani_stanje_trenutnega_uporabnika(stanje)
                bottle.redirect(url_fransize(id_fransize))
        except ValueError:
            napaka = "sprememba mora biti celo število"
            return bottle.template("fransiza.html", fransize=stanje.fransize,
                                   aktualna_fransiza=fransiza,
                                   id_aktualne_fransize=id_fransize,
                                   napaka1=None, napaka2=None, napaka3=napaka)
    if sprememba == "pozicijo":
        oseba.sprememba_pozicije(kolicina_delovno_mesto)
        shrani_stanje_trenutnega_uporabnika(stanje)
        bottle.redirect(url_fransize(id_fransize))


@bottle.post("/odpusti/<id_fransize:int>/<id_osebe:int>/")
def odpusti(id_fransize, id_osebe):
    stanje = stanje_trenutnega_uporabnika()
    fransiza = stanje.fransize[id_fransize]
    oseba = fransiza.osebe[id_osebe]
    fransiza.odpusti_osebo(oseba)
    shrani_stanje_trenutnega_uporabnika(stanje)
    bottle.redirect(url_fransize(id_fransize))


@bottle.error()
def error_404():
    return "Ta stran ne obstaja!"


bottle.run(debug=True, reloader=True)
