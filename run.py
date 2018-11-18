from flask import Flask
app = Flask(__name__)

from flask import render_template, request, redirect, url_for, Flask
from configuraciones import *

import psycopg2
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s"%(host,database,user,passwd,port))
cur = conn.cursor()

@app.route('/')
@app.route('/index')

def index():	
	sql = "select * from canciones"
	cur.execute(sql)
	canciones = cur.fetchall()

	sql = "select * from autores"
	cur.execute(sql)
	autores = cur.fetchall()

	sql = "select * from generos"
	cur.execute(sql)
	generos = cur.fetchall()

	sql = "select * from albumes"
	cur.execute(sql)
	albumes = cur.fetchall()

	return render_template("index.html",canciones = canciones, autores = autores, generos = generos, albumes = albumes)

@app.route('/cancion/<int:id>')	
def cancion(id):
	sql = "select * from Canciones where id = " + str(id)
	cur.execute(sql)
	cancion = cur.fetchall()

	sql = "select Autor_id from Canciones_Autores where Cancion_id = " + str(id)
	cur.execute(sql)
	autor_id = cur.fetchall()
	autor = []
	for i in autor_id: 
		sql = "select * from Autores where id = " + str(i[0]) 
		cur.execute(sql)
		autor.append(cur.fetchall())

	sql = "select Genero_id from Canciones_Generos where Cancion_id = " + str(id)
	cur.execute(sql)
	genero_id = cur.fetchall()
	genero = []
	for i in genero_id: 
		sql = "select * from Generos where id = " + str(i[0]) 
		cur.execute(sql)
		genero.append(cur.fetchall())

	sql = "select Album_id from Canciones_Albumes where Cancion_id = " + str(id)
	cur.execute(sql)
	album_id = cur.fetchall()
	album = []
	for i in album_id: 
		sql = "select * from Albumes where id = " + str(i[0]) 
		cur.execute(sql)
		album.append(cur.fetchall())

	return render_template('cancion.html',autor=autor,cancion=cancion, genero=genero, album=album)

@app.route('/autor/<int:id>')	
def autor(id):
	sql = "select * from Autores where id = " + str(id)
	cur.execute(sql)
	autor = cur.fetchall()

	sql = "select Cancion_id from Canciones_Autores where Autor_id = " + str(id)
	cur.execute(sql)
	cancion_id = cur.fetchall()
	cancion = []
	for i in cancion_id: 
		sql = "select * from Canciones where id = " + str(i[0]) 
		cur.execute(sql)
		cancion.append(cur.fetchall())

	sql = "select Album_id from Canciones_Albumes, Canciones_Autores where Canciones_Albumes.Cancion_id = Canciones_Autores.Cancion_id and Autor_id = " + str(id) + " group by Album_id"
	cur.execute(sql)
	album_id = cur.fetchall()
	album = []
	for i in album_id: 
		sql = "select * from Albumes where id = " + str(i[0]) 
		cur.execute(sql)
		album.append(cur.fetchall())

	

	return render_template('autor.html',autor=autor,cancion=cancion, album=album)

@app.route('/genero/<int:id>')	
def genero(id):
	sql = "select * from Generos where id = " + str(id)
	cur.execute(sql)
	genero = cur.fetchall()

	sql = "select Cancion_id from Canciones_Generos where Genero_id = " + str(id) 
	cur.execute(sql)
	cancion_id = cur.fetchall()
	cancion = []
	for i in cancion_id: 
		sql = "select * from Canciones where id = " + str(i[0]) 
		cur.execute(sql)
		cancion.append(cur.fetchall())

	

	return render_template('genero.html',genero=genero,cancion=cancion)

@app.route('/album/<int:id>')	
def album(id):
	sql = "select * from Albumes where id = " + str(id)
	cur.execute(sql)
	album = cur.fetchall()

	sql = "select Autor_id from Canciones_Autores, Canciones_Albumes where Album_id = " + str(id) + " and Canciones_Autores.Cancion_id=Canciones_Albumes.Cancion_id group by Autor_id" 
	cur.execute(sql)
	autor_id = cur.fetchall()
	autor = []
	for i in autor_id: 
		sql = "select * from Autores where id = " + str(i[0]) 
		cur.execute(sql)
		autor.append(cur.fetchall())

	sql = "select Cancion_id from Canciones_Albumes where Album_id = " + str(id)  
	cur.execute(sql)
	cancion_id = cur.fetchall()
	cancion = []
	for i in cancion_id: 
		sql = "select * from Canciones where id = " + str(i[0]) 
		cur.execute(sql)
		cancion.append(cur.fetchall())
	

	return render_template('album.html',album=album,genero=genero,cancion=cancion, autor=autor)

app.run(port=80)
