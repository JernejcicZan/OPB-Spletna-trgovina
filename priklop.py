from bottle import *

import auth_public as auth
import sqlite3

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) 

import os

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

def rtemplate(*largs, **kwargs):
    """
    Izpis predloge s podajanjem spremenljivke ROOT z osnovnim URL-jem.
    """
    return template(ROOT=ROOT, *largs, **kwargs)

static_dir = "./static"
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)


@get('/')
def index():
    return rtemplate('zacetna.html')

@get('/uporabniki')
def uporabniki_get():
    cur.execute("SELECT * FROM uporabniki")
    return rtemplate('uporabniki.html', uporabniki=cur)

@get('/artikli')
def artikli_get():
    cur.execute("SELECT * FROM artikli")
    return rtemplate('artikli.html', artikli=cur)

@get('/dodaj_uporabnika')
def dodaj_uporabnika():
    return rtemplate('dodaj_uporabnika.html', id='', Ime='', Priimek='', Naslov='', Zaposlen='')


@post('/dodaj_uporabnika')
def dodaj_uporabnika():
    id = request.forms.id
    Ime = request.forms.Ime
    Priimek = request.forms.Priimek
    Naslov = request.forms.Naslov
    Zaposlen = request.forms.Zaposlen
    cur.execute("INSERT INTO uporabniki (id,Ime,Priimek,Naslov,Zaposlen) VALUES (%s, %s, %s, %s, %s)", 
                (id,Ime,Priimek,Naslov,Zaposlen))
    conn.commit()
    redirect('/uporabniki')

@get('/dodaj_artikel')
def dodaj_artikel():
    return rtemplate('dodaj_artikel.html', id='', Izdelek='', Zaloga='', Cena='')


@post('/dodaj_artikel')
def dodaj_artikel():
    id = request.forms.id
    Izdelek = request.forms.Izdelek
    Zaloga = request.forms.Zaloga
    Cena = request.forms.Cena
    cur.execute("INSERT INTO artikli(id,Izdelek,Zaloga,Cena) VALUES(%s,%s,%s,%s)",
                (id,Izdelek,Zaloga,Cena))
    conn.commit()   
    redirect('/artikli')



conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)

