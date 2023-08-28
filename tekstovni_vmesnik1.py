from model1 import Oseba, Stanje, Fransiza

IME_DAT = "stanje.json"
try:
    stanje = Stanje.iz_datoteke(IME_DAT)
except FileNotFoundError:
    stanje = Stanje(fransize=[])


def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def preveri_startost():
    while True:
        vnos = input("starost> ")
        try:
            vrednost = int(vnos)
            if vrednost < 0:
                print("Vnesti morate pozitivno število")
                continue
            break
        except ValueError:
            print("Vnesti morate pozitivno število.")
    return vrednost


def preveri_placo():
    while True:
        vnos = input("mesečna plača> ")
        try:
            vrednost = int(vnos)
            if vrednost < 0:
                print("Vnesti morate pozitivno število")
                continue
            break
        except ValueError:
            print("Vnesti morate pozitivno število.")
    return vrednost


def prevri_spremembo_place(oseba):
    while True:
        vnos = input("Sprememba mesečne plače> ")
        try:
            vrednost = int(vnos)
            if vrednost < 0 and -vrednost > oseba.mesecna_placa:
                print("Plača delavca ne more pasti pod 0")
                continue
            break
        except ValueError:
            print("Vnesti morate število.")
    return vrednost
 

def prikaz_fransize(fransiza):
    return f"{fransiza.lokacija.upper()}"


def prikaz_osebe_0(oseba):
    return f"{oseba.ime_priimek}"
    

def prikaz_osebe_1(oseba):
    return f"{oseba.ime_priimek}, {oseba.pozicija} "
    

def prikaz_osebe_2(oseba):
    return f"{oseba.ime_priimek}, {oseba.mesecna_placa} "


def izberi_fransizo(stanje):
    print("Izberite franšizo:")
    return izberi_moznost(
        [
            (fransiza, prikaz_fransize(fransiza))
            for fransiza in stanje.fransize
        ]
    )


def izberi_osebo_0(fransiza):
    print("Izberite Osebo:")
    return izberi_moznost(
        [(oseba, prikaz_osebe_0(oseba)) for oseba in fransiza.osebe]
    )


def izberi_osebo_1(fransiza):
    print("Izberite Osebo:")
    return izberi_moznost(
        [(oseba, prikaz_osebe_1(oseba)) for oseba in fransiza.osebe]
    )


def izberi_osebo_2(fransiza):
    print("Izberite Osebo:")
    return izberi_moznost(
        [(oseba, prikaz_osebe_2(oseba)) for oseba in fransiza.osebe]
    )


def pozdrav():
    print("Doborodšli v programu za pregled in opravljanje franšiz!")


def pregled_oseb():
    fransiza = izberi_fransizo(stanje)
    if len(fransiza.osebe) == 0:
        print("Tukaj še ne dela nobena oseba")
    for oseba in fransiza.osebe:
        print(f"ime in priimek: {oseba.ime_priimek}, starost: {oseba.starost}, pozicija: {oseba.pozicija}, mesečna plača: {oseba.mesecna_placa}")
    input("Pritisnite enter za nazaj> ")


def dodaj_fransizo():
    print("Vnesite podatke nove franšize.")
    lokacija = input("lokacija> ")
    if stanje.preveri_nove_fransize(lokacija):
        print("Franšiza na tej lokaciji že obstaja")
        input("Pritisnite enter za nazaj>")
    else:    
        nova_fransiza = Fransiza(lokacija, [])
        stanje.dodaj_fransizo(nova_fransiza)


def sprememba_place():
    fransiza = izberi_fransizo(stanje)
    oseba = izberi_osebo_2(fransiza)
    print(f"Trentuna mesečna plača: {oseba.mesecna_placa}")
    kolicina = prevri_spremembo_place(oseba)
    oseba.spremeba_place(kolicina)


def spremeni_pozicijo():
    fransiza = izberi_fransizo(stanje)
    oseba = izberi_osebo_1(fransiza)
    print(f"Trentuna pozicija: {oseba.pozicija}")
    nova_pozicija = input("nova pozicija> ")
    oseba.sprememba_pozicije(nova_pozicija)


def spremeni_lokacijo():
    fransiza = izberi_fransizo(stanje)
    oseba = izberi_osebo_0(fransiza)
    ime = oseba.ime_priimek
    starost = oseba.starost
    placa = oseba.mesecna_placa
    pozicija = oseba.pozicija
    nova_fransiza = input("Kam jo želite premakniti?> ")
    nova_oseba = Oseba(ime, starost, pozicija, placa)
    nova_fransiza.dodaj_osebo(nova_oseba)
    fransiza.osebe.remove(oseba)


def dodaj_osebo():
    ni_fransize = False
    if len(stanje.fransize) == 0:
        ni_fransize = True
        print("Najprej ustavrite fransizo")
        input("Pritisnite enter za nazaj>")
    fransiza = izberi_fransizo(stanje)
    je_drugje = False
    print("Vnesite podatke nove osebe.")
    ime_priimek = input("ime priimek> ")
    for fransiza1 in stanje.fransize:
        if not ni_fransize:
           if fransiza.preveri_ime_osebe(ime_priimek):
              je_drugje = True
              print("Ta osebe že dela v tej franšizi")
              input("Pritisnite enter za nazaj>")
           elif fransiza1.preveri_ime_osebe(ime_priimek):
               je_drugje = True
               print("Ta osebe že dela na drugi lokaciji")
               input("Pritisnite enter za nazaj>")
    if not je_drugje and not ni_fransize:   
        starost = preveri_startost()    
        pozicija = input("pozicija> ")
        mesecna_placa = preveri_placo()
        nova_oseba = Oseba(ime_priimek, starost, pozicija, mesecna_placa)
        fransiza.dodaj_osebo(nova_oseba)


def odpusti_osebo():
    fransiza = izberi_fransizo(stanje)
    oseba = izberi_osebo_0(fransiza)
    fransiza.osebe.remove(oseba)


def izpisi_trenutno_stanje():
    for fransiza in stanje.fransize:
        if len(fransiza.osebe) == 0:
            print(f"{prikaz_fransize(fransiza)}: tukaj še ne dela nobena oseba")
        else:
            print(f"{prikaz_fransize(fransiza)}: mesečni strošek: {fransiza.placa_celotne_fransize()}€, število zaposlenih: {fransiza.stevilo_zaposlenih()}")
    if not stanje.fransize:
        print("Trenutno nimate še nobene franšize, zato najprej eno ustvarite.")


def izberi_moznost(moznosti):
    for i, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        j = preberi_stevilo()
        if 1 <= j <= len(moznosti):
            moznost, _opis = moznosti[j - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moznosti)}.")


def zakljuci_izvajanje():
    stanje.v_datoteko(IME_DAT)
    print("Lep dan še naprej!")
    exit()


def moznosti():
    print("Kaj želite narediti?")
    izbrano_dejanje = izberi_moznost(
        [
            (dodaj_fransizo, "dodal novo franšizo"),
            (dodaj_osebo, "zaposlil novo osebo"),
            (pregled_oseb, "pogledal podatake oseb"),
            (spremeni_pozicijo, "spremenil osebi pozicijo"),
            (sprememba_place, "spremenil osebi plačo"),
            (spremeni_lokacijo,"spremenil osebi lokacijo"),
            (odpusti_osebo, "odpustil osebo"),
            (zakljuci_izvajanje, "zapustil program")
        ]
    )
    izbrano_dejanje()


def tekstovni_vmesnik():
    pozdrav()
    while True:
        izpisi_trenutno_stanje()
        moznosti()


tekstovni_vmesnik()
