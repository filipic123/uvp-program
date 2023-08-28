import json

class Stanje:
    def __init__(self, fransize):
        self.fransize = fransize

    def dodaj_fransizo(self, fransiza):
        self.fransize.append(fransiza)

    def preveri_nove_fransize(self, nova_fransiza):
        for fransiza in self.fransize:
            if fransiza.lokacija == nova_fransiza:
                return True
        return False

    def v_slovar(self):
        return {
            "fransize": [fransiza.v_slovar() for fransiza in self.fransize],
        }

    @staticmethod
    def iz_slovarja(slovar):
        stanje = Stanje(
            [
                Fransiza.iz_slovarja(sl_fransize)
                for sl_fransize in slovar["fransize"]
            ]
        )
        return stanje

    def v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as datoteka:
            slovar = self.v_slovar()
            json.dump(slovar, datoteka, indent=4, ensure_ascii=False)

    @staticmethod
    def iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar = json.load(datoteka)
            return Stanje.iz_slovarja(slovar)


class Fransiza:
    def __init__(self, lokacija, osebe=None):
        self.lokacija = lokacija
        self.osebe = osebe

    def dodaj_osebo(self, oseba):
        self.osebe.append(oseba)

    def preveri_ime_osebe(self, nova_oseba):
        for oseba in self.osebe:
            if oseba.ime_priimek == nova_oseba:
                return True
        return False

    def placa_celotne_fransize(self):
        placa_fransize = 0
        for oseba in self.osebe:
            placa_fransize =  placa_fransize + int(oseba.mesecna_placa)
        return placa_fransize

    def stevilo_zaposlenih(self):
        zaposleni = len(self.osebe)
        return zaposleni
    
    def odpusti_osebo(self, odpuscena_oseba):
        zacetno_stevilo = len(self.osebe)
        for oseba in self.osebe:
            if oseba.ime == odpuscena_oseba:
                self.osebe.remove(odpuscena_oseba)
        if zacetno_stevilo == len(self.osebe):
            return {"oseba": "ta oseba ne dela pri vas"}

    def v_slovar(self):
        return {
            "lokacija": self.lokacija,
            "osebe": [Oseba.v_slovar(oseba) for oseba in self.osebe],
        }

            
    @staticmethod
    def iz_slovarja(slovar):
        return Fransiza(
            slovar["lokacija"],
            [Oseba.iz_slovarja(sl_osebe) for sl_osebe in slovar["osebe"]],           
        )


class Oseba:
    def __init__(self, ime_priimek, starost, pozicija, mesecna_placa):
        self.ime_priimek = ime_priimek
        self.starost = starost
        self.pozicija = pozicija
        self.mesecna_placa = int(mesecna_placa)
    

    def spremeba_place(self, kolicina):
        self.mesecna_placa = self.mesecna_placa +  int(kolicina)
    
    def sprememba_pozicije(self, nova_pozicija):
        self.pozicija = nova_pozicija

    def v_slovar(self):
        return {
            "ime_priimek": self.ime_priimek,
            "starost": self.starost,
            "pozicija": self.pozicija,
            "mesecna_placa": self.mesecna_placa
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Oseba(
            slovar["ime_priimek"],
            slovar["starost"],
            slovar["pozicija"],
            slovar["mesecna_placa"]
        )