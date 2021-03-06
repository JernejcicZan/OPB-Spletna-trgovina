from bottle import *

import auth_public as auth
import sqlite3
from datetime import date,timedelta

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
    cur.execute("SELECT * FROM artikli ORDER BY id")
    return rtemplate('artikli.html', artikli=cur)

@get('/dodaj_uporabnika')
def dodaj_uporabnika():
    return rtemplate('dodaj_uporabnika.html', Ime='', Priimek='', Naslov='', Zaposlen='')



@post('/dodaj_uporabnika')
def dodaj_uporabnika():
    Ime = request.forms.Ime
    Priimek = request.forms.Priimek
    Naslov = request.forms.Naslov
    Zaposlen = request.forms.Zaposlen
    try:
        cur.execute("INSERT INTO uporabniki (  Ime,Priimek,Naslov,Zaposlen) VALUES ( %s, %s, %s, %s)", 
                (Ime,Priimek,Naslov,Zaposlen))
        conn.commit()
    except:
        conn.rollback()
        return rtemplate('dodaj_uporabnika.html',  Ime='', Priimek='', Naslov='', Zaposlen='')
    redirect('{0}uporabniki'.format(ROOT))
    
@get('/dodaj_artikel')
def dodaj_artikel():
    return rtemplate('dodaj_artikel.html', id='', Izdelek='', Zaloga='', Cena='')


@post('/dodaj_artikel')
def dodaj_artikel():
    Izdelek = request.forms.Izdelek
    Zaloga = request.forms.Zaloga
    Cena = request.forms.Cena
    try:
        cur.execute("INSERT INTO artikli(Izdelek,Zaloga,Cena) VALUES(%s,%s,%s)",
                (Izdelek,Zaloga,Cena))
        conn.commit()   
    except:
        conn.rollback()
        return rtemplate('dodaj_artikel.html', Izdelek='', Zaloga='', Cena='')
    redirect('{0}artikli'.format(ROOT))

@get('/artikli/naroci/<id>')
def naroci_izdelek_get(id):
    cur.execute("SELECT id FROM artikli WHERE id = %s" %int(id))
    id_izdelka = cur.fetchone()[0]
    return rtemplate('oddaj_narocilo.html',id_uporabnika='', id_izdelka=id_izdelka, kolicina='',posiljanje='',nacin_placila=''  )

@post('/artikli/naroci/<id_izdelka>')
def naroci_izdelek_post(id_izdelka):
    uporabnik = request.forms.id_uporabnika
    izdelek = id_izdelka
    kolicina = request.forms.kolicina
    posiljanje = request.forms.posiljanje
    nacin_placila = request.forms.nacin_placila
    try:
        cur.execute("SELECT Cena FROM artikli WHERE id = %s" %int(izdelek))
        cena_izdelka = cur.fetchone()[0]
        cur.execute("UPDATE artikli SET Zaloga = Zaloga - %s WHERE id = %s",(int(kolicina),int(izdelek)))
        cur.execute("INSERT INTO narocila(stevilka_narocila, uporabnik,izdelek,datum,kolicina,posiljanje,rok_placila,nacin_placila, cena) VALUES(DEFAULT, %s,%s,%s,%s,%s,%s,%s,%s)",
                    (uporabnik, izdelek, date.today(), kolicina,posiljanje,date.today()+timedelta(days=10), nacin_placila, int(kolicina)*cena_izdelka))
        conn.commit()   
    except: 
        conn.rollback()
        return rtemplate('oddaj_narocilo.html', id_uporabnika='',id_izdelka=id_izdelka,kolicina='',posiljanje='',nacin_placila='')
    redirect('{0}narocila'.format(ROOT))

        


@get('/oddaj_narocilo')
def oddaj_narocilo():
   return rtemplate('oddaj_narocilo.html', id_uporabnika='',id_izdelka='',kolicina='',posiljanje='',nacin_placila='')

@post('/oddaj_narocilo')
def oddaj_narocilo():
    uporabnik = request.forms.id_uporabnika
    izdelek = request.forms.id_izdelka
    kolicina = request.forms.kolicina
    posiljanje = request.forms.posiljanje
    nacin_placila = request.forms.nacin_placila
    try:
        cur.execute("SELECT Cena FROM artikli WHERE id = %s" %int(izdelek))
        cena_izdelka = cur.fetchone()[0]
        cur.execute("UPDATE artikli SET Zaloga = Zaloga - %s WHERE id = %s",(int(kolicina),int(izdelek)))
        cur.execute("INSERT INTO narocila(stevilka_narocila, uporabnik,izdelek,datum,kolicina,posiljanje,rok_placila,nacin_placila, cena) VALUES(DEFAULT, %s,%s,%s,%s,%s,%s,%s,%s)",
                    (uporabnik, izdelek, date.today(), kolicina,posiljanje,date.today()+timedelta(days=10), nacin_placila, int(kolicina)*cena_izdelka))
        conn.commit()   
    except: 
        conn.rollback()
        return rtemplate('oddaj_narocilo.html', id_uporabnika='',id_izdelka='',kolicina='',posiljanje='',nacin_placila='')
    redirect('{0}narocila'.format(ROOT))

      

@get('/narocila')
def narocila():
    cur.execute("SELECT * FROM narocila")
    return rtemplate('narocila.html', narocila=cur)

@get('/povecaj_zalogo')
def povecaj_zalogo():
    return rtemplate('povecaj_zalogo.html', id='', kolicina='')


@post('/povecaj_zalogo')
def povecaj():
    id = request.forms.id
    kolicina = request.forms.kolicina 
    try:
        cur.execute("UPDATE artikli SET Zaloga = Zaloga + %s WHERE id = %s",(int(kolicina), int(id)))
        conn.commit()
    except:
        conn.rollback()
        return rtemplate('povecaj_zalogo.html', id='', kolicina='')

    redirect('{0}artikli'.format(ROOT))


conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=DB_PORT)
#conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) 
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=True)

