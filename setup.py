from configuraciones import *
import psycopg2
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s"%(host,database,user,passwd,port))


cur = conn.cursor()
sql ="""DROP SCHEMA public CASCADE;
CREATE SCHEMA public;"""

cur.execute(sql)

sql ="""
CREATE TABLE Canciones
           (id serial PRIMARY KEY, nombre varchar(80), duracion integer);
"""

cur.execute(sql)


sql ="""
CREATE TABLE Autores
           (id serial PRIMARY KEY, nombre varchar(40));
"""

cur.execute(sql)

sql ="""
CREATE TABLE Canciones_Autores
           (Cancion_id integer, Autor_id integer);
"""

cur.execute(sql)

sql ="""
CREATE TABLE  Generos
           (id serial PRIMARY KEY, nombre varchar(140));
"""

cur.execute(sql)

sql ="""
CREATE TABLE Canciones_Generos
           (Cancion_id integer, Genero_id integer);
"""

cur.execute(sql)

sql = """
CREATE TABLE Albumes
           (id serial PRIMARY KEY, nombre varchar(140), ano integer);
"""

cur.execute(sql)

sql = """
CREATE TABLE Canciones_Albumes
           (Cancion_id integer, Album_id integer);
"""

cur.execute(sql)

sql ="""
CREATE TABLE Usuarios
        (id serial PRIMARY KEY, name varchar(40), pass varchar(100));
"""

cur.execute(sql)


conn.commit()
cur.close()
conn.close()