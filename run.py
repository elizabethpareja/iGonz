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

	error1 = None

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
		print(Autores_Cancion_nueva, Generos_Cancion_nueva, Albumes_Cancion_nueva)

		if album_nuevo != "" or ano_nuevo != "":
			try:
				int(ano_nuevo)
			except ValueError:
				error1='Rellene los campos necesarios y correctamente.'
				return error()
			if album_nuevo!= "" and ano_nuevo!= "":
				sql = "insert into Albumes (nombre,ano) values ('%s','%s') returning id" %(album_nuevo,ano_nuevo)
				cur.execute(sql)
			else:
				error1 = "Rellene los campos necesarios."
				return error()

		if  autor_nuevo!="":
			sql = "insert into Autores (nombre) values ('%s') returning id" %(autor_nuevo)
			cur.execute(sql)

		if  genero_nuevo!="":
			sql = "insert into Generos (nombre) values ('%s') returning id" %(genero_nuevo)
			cur.execute(sql)


		if cancion_nueva!="" or cancion_seg_nueva!= "" or Autores_Cancion_nueva or Generos_Cancion_nueva or Albumes_Cancion_nueva:
			try:
				int(cancion_seg_nueva)
			except ValueError:
				error1='Rellene los campos necesarios y correctamente.'
				return error()

			if  cancion_nueva!="" and cancion_seg_nueva!= "" and Autores_Cancion_nueva and Generos_Cancion_nueva and Albumes_Cancion_nueva:
				sql = "insert into Canciones (nombre, duracion) values ('%s','%s') returning id" %(cancion_nueva, str(cancion_seg_nueva))
				cur.execute(sql)
				id_cancion = cur.fetchall()

				for i in Autores_Cancion_nueva:
					sql = "insert into Canciones_Autores (cancion_id, autor_id) values ('%s','%s') " %(id_cancion[0][0], i)
					cur.execute(sql)
				for i in Generos_Cancion_nueva:
					sql = "insert into Canciones_Generos (cancion_id, genero_id) values ('%s','%s') " %(id_cancion[0][0], i)
					cur.execute(sql)
				for i in Albumes_Cancion_nueva:
					sql = "insert into Canciones_Albumes (cancion_id, album_id) values ('%s','%s') " %(id_cancion[0][0], i)
					cur.execute(sql)
			else:
				error1='Rellene los campos necesarios y correctamente.'
				return error()


		conn.commit()
		succ = "Se ha agregado satisfactoriamente."
		return success(succ)
	return render_template("index.html",canciones = canciones, autores = autores, generos = generos, albumes = albumes, error1 = error1)

@app.route('/cancion/<int:id>', methods=["GET", "POST"])	
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
	#if Borrar Canción:
	if request.method == "POST":
		sql = "delete from canciones where id = " + str(id)
		cur.execute(sql)
		sql = "delete from Canciones_Autores where Cancion_id = " + str(id)
		cur.execute(sql)
		sql = "delete from Canciones_Albumes where Cancion_id = " + str(id)
		cur.execute(sql)
		sql = "delete from Canciones_Generos where Cancion_id = " + str(id)
		cur.execute(sql)
		conn.commit()
		succ = "Cancion eliminada exitosamente."
		return success(succ)

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
def success(succ):
	return render_template("success.html", succ = succ)

@app.route('/error')
def error():
	return render_template("error.html")

@app.route('/editar%3id_cancion%3D<int:id_cancion>', methods=["GET", "POST"])
def editar(id_cancion):
	id_cancion = str(id_cancion)

	sql = "select * from canciones where id = " + id_cancion
	cur.execute(sql)
	cancion = cur.fetchall()

	sql = "select autor_id from Canciones_Autores where cancion_id = " + id_cancion
	cur.execute(sql)
	autores_id = cur.fetchall()

	sql = "select album_id from Canciones_Albumes where cancion_id = " + id_cancion
	cur.execute(sql)
	albumes_id = cur.fetchall()

	sql = "select genero_id from Canciones_Generos where cancion_id = " + id_cancion
	cur.execute(sql)
	generos_id = cur.fetchall()

	sql = "select * from autores"
	cur.execute(sql)
	autores = cur.fetchall()

	sql = "select * from generos"
	cur.execute(sql)
	generos = cur.fetchall()

	sql = "select * from albumes"
	cur.execute(sql)
	albumes = cur.fetchall()

	error1 = None

	if request.method == "POST":
		
		cancion_nueva = request.form["Cancion_nueva"]
		cancion_seg_nueva = request.form["Cancion_seg_nueva"]
		Autores_Cancion_nueva = request.form.getlist("AUTORES")
		Generos_Cancion_nueva = request.form.getlist("GENEROS")
		Albumes_Cancion_nueva = request.form.getlist("ALBUMES")


		if cancion_nueva!="" or cancion_seg_nueva!= "" or Autores_Cancion_nueva or Generos_Cancion_nueva or Albumes_Cancion_nueva:
			try:
				int(cancion_seg_nueva)
			except ValueError:
				error1='Rellene los campos necesarios y correctamente.'
				return error()

			if  cancion_nueva!="" and cancion_seg_nueva!= "" and Autores_Cancion_nueva and Generos_Cancion_nueva and Albumes_Cancion_nueva:
				sql = "update Canciones set nombre = '%s', duracion = '%s' where id = %s" %(cancion_nueva, str(cancion_seg_nueva), id_cancion)
				cur.execute(sql)
				sql = "delete from Canciones_Autores where cancion_id = " + id_cancion
				cur.execute(sql)
				sql = "delete from Canciones_Generos where cancion_id = " + id_cancion
				cur.execute(sql)
				sql = "delete from Canciones_Albumes where cancion_id = " + id_cancion
				cur.execute(sql)
				for i in Autores_Cancion_nueva:
					sql = "insert into Canciones_Autores (cancion_id, autor_id) values ('%s','%s') " %(id_cancion, i)
					cur.execute(sql)
				for i in Generos_Cancion_nueva:
					sql = "insert into Canciones_Generos (cancion_id, genero_id) values ('%s','%s') " %(id_cancion, i)
					cur.execute(sql)
				for i in Albumes_Cancion_nueva:
					sql = "insert into Canciones_Albumes (cancion_id, album_id) values ('%s','%s') " %(id_cancion, i)
					cur.execute(sql)
			else:
				error1='Rellene los campos necesarios y correctamente.'
				return error()


		conn.commit()
		succ = "Se ha agregado satisfactoriamente."
		return success(succ)
	return render_template("editar.html", cancion = cancion, autores = autores, generos = generos, albumes = albumes, error1 = error1, autores_id = autores_id, albumes_id = albumes_id, generos_id = generos_id)


app.run(port=80)