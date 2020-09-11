import sqlite3
import csv
import auth_public as auth

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki


def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        koda = f.read()
        cur.execute(koda)



def uvoziCSV(cur, tabela):
    with open('podatki/{0}.csv'.format(tabela)) as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
        tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstice)



conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 


uvoziSQL(cur, 'trgovina.sql')
uvoziCSV(cur, 'uporabniki')
uvoziCSV(cur, 'artikli')
conn.commit()


