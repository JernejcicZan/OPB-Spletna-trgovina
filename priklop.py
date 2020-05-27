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
    return('Začetna stran')

@get('/uporabniki')
def uporabniki_get():
    cur.execute("SELECT * FROM uporabniki")
    return rtemplate('uporabniki.html', uporabniki=cur)

@get('/artikli')
def artikli_get():
    cur.execute("SELECT * FROM artikli")
    return rtemplate('artikli.html', artikli=cur)


@post('/uporabniki/dodaj')
def dodaj_uporabnika():
    id = request.get.forms('id')
    Ime = request.get.forms('Ime')
    Priimek = request.get.forms('Priimek')
    Naslov = request.get.forms('Naslov')
    Zaposlen = request.get.forms('Zaposlen')
    cur.execute("INSERT INTO uporabniki(id,Ime,Priimek,Naslov,Zaposlen) VALUES(,?,?,?,?)",(id, Ime,Priimek,Naslov,Zaposlen))
    redirect('/uporabniki')

@post('/artikli/dodaj')
def dodaj_artikel():
    id = request.get.forms('id')
    Izdelek = request.get.forms('Izdelek')
    Cena = request.get.forms('Cena')
    Zaloga = request.get.forms('Zaloga')
    cur.execute("INSERT INTO artikli(id,Izdelek,Zaloga,Cena) VALUES(%s,%s,%s,%s)",(id,Izdelek,Zaloga,Cena))
    conn.commit()
        
    redirect('/artikli')



conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)

