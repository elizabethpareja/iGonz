from flask import Flask
app = Flask(__name__)

from flask import render_template, request, redirect, url_for, Flask
from configuraciones import *

import psycopg2
conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s port=%s"%(host,database,user,passwd,port))
cur = conn.cursor()

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])

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

	if request.method == "POST":
		cancion_nueva = request.form["Cancion_nueva"]
		cancion_seg_nueva = request.form["Cancion_seg_nueva"]
		autor_nuevo = request.form["Autor_nuevo"]
		genero_nuevo = request.form["Genero_nuevo"]
		album_nuevo = request.form["Album_nuevo"]
		ano_nuevo = request.form["Ano_nuevo"]
		Autores_Cancion_nueva = request.form.getlist("AUTORES")
		Generos_Cancion_nueva = request.form.getlist("GENEROS")
		Albumes_Cancion_nueva = request.form.getlist("ALBUMES")
		sql = "select max(id) from canciones"
		cur.execute(sql)
		id_cancion = cur.fetchall()
		id_cancion = str(int(id_cancion[0][0]) + 1)

		if album_nuevo!= "" and ano_nuevo!= "":
			sql = "insert into Albumes (nombre,ano) values ('%s','%s') returning id" %(album_nuevo,ano_nuevo)
			cur.execute(sql)
		

		if  autor_nuevo!="":
			sql = "insert into Autores (nombre) values ('%s') returning id" %(autor_nuevo)
			cur.execute(sql)

		if  genero_nuevo!="":
			sql = "insert into Generos (nombre) values ('%s') returning id" %(genero_nuevo)
			cur.execute(sql)

		if  cancion_nueva!="" and cancion_seg_nueva!= "" and Autores_Cancion_nueva!= None and Generos_Cancion_nueva!= None and Albumes_Cancion_nueva!= None:
			sql = "insert into Canciones (nombre, duracion) values ('%s','%s') returning id" %(cancion_nueva, str(cancion_seg_nueva))
			cur.execute(sql)
			for i in Autores_Cancion_nueva:
				sql = "insert into Canciones_Autores (cancion_id, autor_id) values ('%s','%s') " %(id_cancion, i[0])
				cur.execute(sql)
			for i in Generos_Cancion_nueva:
				sql = "insert into Canciones_Generos (cancion_id, genero_id) values ('%s','%s') " %(id_cancion, i[0])
				cur.execute(sql)
			for i in Albumes_Cancion_nueva:
				sql = "insert into Canciones_Albumes (cancion_id, album_id) values ('%s','%s') " %(id_cancion, i[0])
				cur.execute(sql)

		conn.commit()
		return success()
	
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

@app.route('/success')
def success():
	return render_template("success.html")

app.run(port=80)
