DROP TABLE IF EXISTS uporabniki;
DROP TABLE IF EXISTS artikli;
DROP TABLE IF EXISTS narocila;


CREATE TABLE uporabniki (
    id INTEGER PRIMARY KEY,
    Ime TEXT NOT NULL,
    Priimek TEXT NOT NULL,
    Naslov TEXT NOT NULL,
    Zaposlen BOOLEAN
);

CREATE TABLE artikli (
    id INTEGER PRIMARY KEY,
    Izdelek TEXT NOT NULL,
    Zaloga INTEGER,
    Cena DECIMAL NOT NULL
);

CREATE TABLE narocila(
    uporabnik INTEGER  REFERENCES uporabniki(id),
    izdelek INTEGER REFERENCES artikli(id),
    datum DATE,
    kolicina INTEGER,
    posiljanje BOOLEAN, 
    rok_placila DATE,
    nacin_placila TEXT,
    popust DECIMAL,
    cena DECIMAL
);