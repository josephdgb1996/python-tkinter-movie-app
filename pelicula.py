import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3


class Pelicula:
    db_name = 'pelicula.db'
    conn = sqlite3.connect('pelicula.db')

    def __init__(self):
        # ventana tk
        window = Tk()

        # creo base de datos
        self.createDatabase()

        # configuraciones ventana
        window.configure(bg='blue')
        canvas = tk.Canvas(window, height=700, width=800)
        canvas.pack()

        background_image = tk.PhotoImage(file="inicio.png")
        background_label = tk.Label(window, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        # frame = tk.Frame(window,bg="blue")
        # frame.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

        # Agregando titulos
        window.title('Aplicacion Peliculas')

        # Agregando Menu
        menu = Menu(window)
        window.config(menu=menu)
        movieMenu = Menu(menu)
        menu.add_cascade(label='Pelicula', menu=movieMenu)
        movieMenu.add_command(label='Nueva Pelicula',
                              command=self.openNewMovie)
        movieMenu.add_command(label='Listar Peliculas',
                              command=self.openListMovies)
        movieMenu.add_command(label='Rankear Pelicula',
                              command=self.openSetRanking)
        movieMenu.add_command(label='Listar Ranking',
                              command=self.openListRanking)

        clientMenu = Menu(menu)
        menu.add_cascade(label='Cliente', menu=clientMenu)
        clientMenu.add_command(label='Nuevo Cliente',
                               command=self.openNewClient)
        clientMenu.add_command(label='Listar Clientes',
                               command=self.openListClients)

        # dibujando el window
        window.mainloop()

        super().__init__()

    def createDatabase(self):
        c = self.conn.cursor()

        c.execute('''
                CREATE TABLE IF NOT EXISTS pelicula(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre VARCHAR(100) UNIQUE NOT NULL,
                    duracion INTEGER NOT NULL)
        ''')
        c.execute('''
                CREATE TABLE IF NOT EXISTS cliente(
                    cedula VARCHAR(10) PRIMARY KEY UNIQUE NOT NULL,
                    nombre VARCHAR(50) NOT NULL,
                    apellido VARCHAR(50) NOT NULL)
        ''')
        c.execute('''
                CREATE TABLE IF NOT EXISTS ranking(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    puntaje INTEGER NOT NULL,
                    clienteId VARCHAR(10) NOT NULL,
                    peliculaId INTEGER NOT NULL,
                    FOREIGN KEY (peliculaId) REFERENCES pelicula(id),
                    FOREIGN KEY (clienteId) REFERENCES cliente(cedula) )
        ''')

    def openListRanking(self):
        window = Tk()
        window.geometry("500x500")
        window.configure(bg='#13A5F6')
        window.title('Lista Ranking')

        c = self.conn.cursor()
        sql = "SELECT C.cedula, C.nombre,C.apellido,P.nombre,R.puntaje FROM ranking R JOIN pelicula P ON R.peliculaId = P.id JOIN cliente C ON C.cedula = R.clienteId"

        # rankings
        rankings = c.execute(sql).fetchall()
        print(rankings)

        cols = ('Cedula', 'Nombre','Apellido','Pelicula','Puntaje')
        listBox = ttk.Treeview(window, columns=cols, show='headings')

        for col in cols:
            listBox.heading(col, text=col)
            listBox.grid(row=1, column=0, columnspan=2)
        
        listBox.pack(fill="both", expand=True)

        for ranking in rankings:
            listBox.insert("", "end", values=(
                ranking[0], ranking[1], ranking[2], ranking[3], ranking[4]))


    def openListMovies(self):
        window = Tk()
        window.geometry("500x500")
        window.configure(bg='#13A5F6')
        window.title('Peliculas')

        sql = "SELECT * FROM pelicula"
        c = self.conn.cursor()

        # peliculas
        movies = c.execute(sql).fetchall()

        cols = ('ID', 'NOMBRE', 'DURACION')
        listBox = ttk.Treeview(window, columns=cols, show='headings')

        for col in cols:
            listBox.heading(col, text=col)
            listBox.grid(row=1, column=0, columnspan=2)

        listBox.pack(fill="both", expand=True)

        for movie in movies:
            listBox.insert("", "end", values=(movie[0], movie[1], movie[2]))

    def openNewMovie(self):
        # configuraciones ventana
        window = Tk()
        window.geometry("500x500")
        window.configure(bg='#13A5F6')
        window.title('Agregar nueva Pelicula')

        nombre = Label(window, text="Nombre").place(x=30, y=50)
        duracion = Label(window, text="Duracion").place(x=30, y=90)

        nombreEntry = Entry(window)
        duracionEntry = Entry(window)

        nombreEntry.place(x=95, y=50)
        duracionEntry.place(x=95, y=90)

        submit = Button(window, text="Crear Cliente", command=lambda: self.createMovie(
            nombreEntry, duracionEntry)).place(x=30, y=130)

    def openSetRanking(self):

        # configuraciones ventana
        window = Tk()
        window.configure(bg='#13A5F6')
        window.geometry("500x500")
        window.title('Agregar Ranking')

        cedula = Label(window, text="Cedula").place(x=30, y=50)
        peliculaId = Label(window, text="Pelicula ID").place(x=30, y=90)
        puntaje = Label(window, text="Puntaje").place(x=30, y=130)

        cedulaEntry = Entry(window)
        peliculaIdEntry = Entry(window)
        puntajeEntry = Entry(window)

        cedulaEntry.place(x=95, y=50)
        peliculaIdEntry.place(x=95, y=90)
        puntajeEntry.place(x=95, y=130)

        submit = Button(window, text="Insertar Ranking", command=lambda: self.createRanking(
            cedulaEntry, peliculaIdEntry, puntajeEntry)).place(x=30, y=170)

    def openNewClient(self):
        # configuraciones ventana
        window = Tk()
        window.configure(bg='#13A5F6')
        window.geometry("500x500")
        window.title('Agregar nueva Pelicula')

        cedula = Label(window, text="Cedula").place(x=30, y=50)
        nombre = Label(window, text="Nombre").place(x=30, y=90)
        apellido = Label(window, text="Apellido").place(x=30, y=130)

        cedulaEntry = Entry(window)
        nombreEntry = Entry(window)
        apellidoEntry = Entry(window)

        cedulaEntry.place(x=95, y=50)
        nombreEntry.place(x=95, y=90)
        apellidoEntry.place(x=95, y=130)

        submit = Button(window, text="Crear Cliente", command=lambda: self.createClient(
            cedulaEntry, nombreEntry, apellidoEntry)).place(x=30, y=170)

    def createMovie(self, nombreEntry, duracionEntry):
        nombre = str(nombreEntry.get())
        duracion = duracionEntry.get()
        # validaciones
        if(nombre == "" or duracion == ""):
            return messagebox.showinfo(title="Validacion", message="No se aceptan campos vacios")

        try:
            duracionInt = int(duracion)
        except ValueError:
            return messagebox.showinfo(title="Validacion", message="El campo duracion debe ser numerico")

        sql = "INSERT INTO pelicula (nombre,duracion) VALUES('{}',{})".format(
            nombre, duracionInt)
        c = self.conn.cursor()

        try:
            c.execute(sql)
            self.conn.commit()
        except:
            return messagebox.showwarning(title="Pelicula", message="Ya existe una pelicula con este nombre")

        messagebox.showinfo(
            title="Pelicula", message="Pelicula creada con exito")

    def openListClients(self):
        window = Tk()
        window.geometry("500x500")
        window.configure(bg='#13A5F6')
        window.title('Clientes')

        sql = "SELECT * FROM cliente"
        c = self.conn.cursor()

        # clientes
        clients = c.execute(sql).fetchall()

        cols = ('CEDULA', 'NOMBRE', 'APELLIDO')
        listBox = ttk.Treeview(window, columns=cols, show='headings')

        for col in cols:
            listBox.heading(col, text=col)
            listBox.grid(row=1, column=0, columnspan=2)

        listBox.pack(fill="both", expand=True)

        for client in clients:
            listBox.insert("", "end", values=(
                client[0], client[1], client[2]))

    def createRanking(self, cedulaEntry, peliculaIdEntry, puntajeEntry):
        cedula = str(cedulaEntry.get())
        peliculaId = peliculaIdEntry.get()
        puntaje = puntajeEntry.get()

        if(cedula == '' or peliculaId == '' or puntaje == ''):
            return messagebox.showinfo(title="Validacion", message="No se aceptan campos vacios")

        try:
            puntajeInt = int(puntaje)
        except ValueError:
            return messagebox.showinfo(title="Validacion", message="El campo duracion debe ser numerico")

        if puntajeInt > 10 or puntajeInt < 0:
            return messagebox.showinfo(title="Validacion", message="El puntaje debe ser entre 1 y 10")

        c = self.conn.cursor()
        sqlCheck = "SELECT clienteId,peliculaId FROM ranking WHERE clienteId = {} AND peliculaId = {}  ".format(
            cedula, peliculaId)
        sqlcheckCedula = "SELECT * from cliente WHERE cedula = {}".format(
            cedula)
        sqlcheckPelicula = "SELECT * from pelicula WHERE id = {}".format(
            peliculaId)

        checkPelicula = c.execute(sqlCheck).fetchall()
        checkCedula = c.execute(sqlcheckCedula).fetchall()
        checkPleicula = c.execute(sqlcheckPelicula).fetchall()

        c = self.conn.cursor()

        if checkCedula == []:
            return messagebox.showwarning(title="Error", message="Este cliente no existe")
        if checkPleicula == []:
            return messagebox.showwarning(title="Error", message="Esta pelicula no existe")
        
        if checkPelicula == []:
            try:
                c.execute("INSERT INTO ranking (puntaje,clienteId,peliculaId) VALUES({},{},{})".format(puntajeInt,cedula,peliculaId))
                self.conn.commit()
            except:
                return messagebox.showwarning(title="Error", message="Error al crear ranking")
        else:
            return messagebox.showinfo(title="Ranking", message="El usuario no puede puntuar 2 veces la misma pelicula")

        messagebox.showinfo(
            title="Cliente", message="Pelicula Rankeada")

    def createClient(self, cedulaEntry, nombreEntry, apellidoEntry):
        cedula = str(cedulaEntry.get())
        nombre = str(nombreEntry.get())
        apellido = str(apellidoEntry.get())

        sql = "INSERT INTO cliente (cedula,nombre,apellido) VALUES('{}','{}','{}')".format(
            cedula, nombre, apellido)
        c = self.conn.cursor()

        try:
            c.execute(sql)
            self.conn.commit()
        except:
            return messagebox.showwarning(title="Cliente", message="Ya existe un cliente con esta cedula")

        messagebox.showinfo(
            title="Cliente", message="Cliente creado con exito")


Pelicula()
