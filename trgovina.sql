DROP TABLE IF EXISTS uporabniki;
DROP TABLE IF EXISTS izdelki;

CREATE TABLE uporabniki (
    id INTEGER PRIMARY KEY,
    ime CHAR NOT NULL,
    priimek CHAR NOT NULL,
    naslov CHAR NOT NULL,
    zaposleni BOOLEAN
);

CREATE TABLE artikli (
    id INTEGER PRIMARY KEY
    izdelek CHAR NOT NULL,
    zaloga INTEGER,
    cena DECIMAL NOT NULL
);