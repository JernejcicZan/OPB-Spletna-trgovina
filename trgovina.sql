DROP TABLE IF EXISTS uporabniki CASCADE;
DROP TABLE IF EXISTS artikli CASCADE;
DROP TABLE IF EXISTS narocila CASCADE;


CREATE TABLE uporabniki (
    id SERIAL PRIMARY KEY,
    Ime TEXT NOT NULL,
    Priimek TEXT NOT NULL,
    Naslov TEXT NOT NULL,
    Zaposlen BOOLEAN
);

CREATE TABLE artikli (
    id SERIAL PRIMARY KEY,
    Izdelek TEXT NOT NULL,
    Zaloga INTEGER,
    Cena DECIMAL NOT NULL
);

CREATE TABLE narocila(
    stevilka_narocila SERIAL PRIMARY KEY,
    uporabnik INTEGER  REFERENCES uporabniki(id),
    izdelek INTEGER REFERENCES artikli(id),
    datum DATE,
    kolicina INTEGER,
    posiljanje BOOLEAN, 
    rok_placila DATE,
    nacin_placila TEXT,
    cena DECIMAL
);