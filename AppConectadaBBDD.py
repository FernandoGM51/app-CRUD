"""" 
	App de prueba para trabajo con CRUD, BBDD, y la librería tkinter

"""

from tkinter import *
from tkinter import messagebox
import sqlite3

#------------------Funciones------------------------



def conexionBBDD():

	miConexion=sqlite3.connect("Usuarios")
	
	miCursor=miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE DATOS_USUARIOS(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE_USUARIO VARCHAR(50),
			PASSWORD VARCHAR(50),
			APELLIDO VARCHAR(30),
			DIRECCION VARCHAR(50),
			COMENTARIOS VARCHAR(100))
			''')

		messagebox.showinfo("BBDD", "BBDD creada con éxito")

	except:
		messagebox.showwarning("ATENCION", "BBDD ya existente!")


def salirApp():

	valor=messagebox.askquestion("Salir", "¿Desea salir de la aplicacion?")

	if(valor=="yes"):
		root.destroy()


def limpiarCampos():

	miNombre.set("")
	miId.set("")
	miApellido.set("")
	miDireccion.set("")
	miPass.set("")
	textoComentario.delete(1.0, END) #forma de setear a 0 todo el Text. Desde la pos 1 hasta el final


def crear():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	"""miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL, '" + miNombre.get() +
	"','" + miPass.get() +
	"','" + miApellido.get() +
	"','" + miDireccion.get() +
	"','" + textoComentario.get("1.0", END) + "')")"""
	#en lugar del cod anterior, usaremos una consulta parametrizada:
	datos=miNombre.get(), miPass.get(), miApellido.get(), miDireccion.get(), textoComentario.get("1.0", END)

	miCursor.execute("INSERT INTO DATOS_USUARIOS VALUES(NULL,?,?,?,?,?)", datos) #no uso execute many pq se agrega 1 solo reg


	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro agregado con éxito")


def leer():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	miCursor.execute("SELECT * FROM DATOS_USUARIOS WHERE ID= " + miId.get())
	elUsuario=miCursor.fetchall()

	for usuario in elUsuario:

		miId.set(usuario[0])
		miNombre.set(usuario[1])
		miPass.set(usuario[2])
		miApellido.set(usuario[3])
		miDireccion.set(usuario[4])
		textoComentario.insert(1.0, usuario[5]) #1er param: que inserte la info desde el 1er caracter

		miConexion.commit()


def actualizar():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	"""miCursor.execute("UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO='" + miNombre.get() +
		"',PASSWORD='" + miPass.get() +
		"',APELLIDO='" + miApellido.get() +
		"',DIRECCION='" + miDireccion.get() +
		"',COMENTARIOS='" + textoComentario.get("1.0", END) +
		"' WHERE ID=" + miId.get())"""
	#tmb lo haremos parametrizado
	datos=miNombre.get(), miPass.get(), miApellido.get(), miDireccion.get(), textoComentario.get("1.0", END)

	miCursor.execute("UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO=?, PASSWORD=?, APELLIDO=?, DIRECCION=?, COMENTARIOS=? " +
		"WHERE ID=" + miId.get(), datos)

	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro actualizado con éxito")


def eliminar():
	miConexion=sqlite3.connect("Usuarios")
	miCursor=miConexion.cursor()

	miCursor.execute("DELETE FROM DATOS_USUARIOS WHERE ID=" + miId.get())

	miConexion.commit()

	messagebox.showinfo("BBDD", "Registro borrado con éxito")





root=Tk()

#------------------Menu--------------------(el menu no está adentro de ningun frame)
barraMenu=Menu(root)
root.config(menu=barraMenu, width=300, height=300)

bbddMenu=Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Conectar", command=conexionBBDD)
bbddMenu.add_command(label="Salir", command=salirApp)

borrarMenu=Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Borrar Campos", command=limpiarCampos)

crudMenu=Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Crear", command=crear)
crudMenu.add_command(label="Leer", command=leer)
crudMenu.add_command(label="Actualizar", command=actualizar)
crudMenu.add_command(label="Borrar", command=eliminar)

ayudaMenu=Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Licencia")
ayudaMenu.add_command(label="Acerca de...")

#ahora meter esos submenus dentro de la barra menu ppal
barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)


#------------------Labels y Entrys--------------------(dentro del 1er frame)

miFrame=Frame(root)
miFrame.pack()

#necesitamos una variable de tipo string por cada entry(menos el text)
miId=StringVar()
miNombre=StringVar()
miApellido=StringVar()
miPass=StringVar()
miDireccion=StringVar()

cuadroId=Entry(miFrame, textvariable=miId)
cuadroId.grid(row=0, column=1, padx=10, pady=10)

cuadroNombre=Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
cuadroNombre.config(fg="red", justify="right")

cuadroPass=Entry(miFrame, textvariable=miPass)
cuadroPass.grid(row=2, column=1, padx=10, pady=10)
cuadroPass.config(show="x")

cuadroApellido=Entry(miFrame, textvariable=miApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10)

cuadroDireccion=Entry(miFrame, textvariable=miDireccion)
cuadroDireccion.grid(row=4, column=1, padx=10, pady=10)

textoComentario=Text(miFrame, width=16, height=5)
textoComentario.grid(row=5, column=1, padx=10, pady=10)
scrollVert=Scrollbar(miFrame, command=textoComentario.yview)
scrollVert.grid(row=5, column=2, sticky="nsew")
textoComentario.config(yscrollcommand=scrollVert.set)

#labels

idLabel=Label(miFrame, text="Id:")
idLabel.grid(row=0, column=0, padx=10, pady=10, sticky="e")

nombreLabel=Label(miFrame, text="Nombre:")
nombreLabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")

passLabel=Label(miFrame, text="Password:")
passLabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")

apellidoLabel=Label(miFrame, text="Apellido:")
apellidoLabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")

direccionLabel=Label(miFrame, text="Direccion:")
direccionLabel.grid(row=4, column=0, padx=10, pady=10, sticky="e")

comentarioLabel=Label(miFrame, text="Comentarios:")
comentarioLabel.grid(row=5, column=0, padx=10, pady=10, sticky="e")


#--------------------------Buttons---------------------------(dentro del 2do frame)

miFrame2=Frame(root)
miFrame2.pack()

botonCrear=Button(miFrame2, text="Create", command=crear)
botonCrear.grid(row=0, column=0, padx=10, pady=10, sticky="e")

botonLeer=Button(miFrame2, text="Read", command=leer)
botonLeer.grid(row=0, column=1, padx=10, pady=10, sticky="e")

botonActualizar=Button(miFrame2, text="Update", command=actualizar)
botonActualizar.grid(row=0, column=2, padx=10, pady=10, sticky="e")

botonBorrar=Button(miFrame2, text="Delete", command=eliminar)
botonBorrar.grid(row=0, column=3, padx=10, pady=10, sticky="e")









root.mainloop()

