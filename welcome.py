import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from db import *
from inquilinos import Inquilinos
from propiedades import Propiedades
from contratos import Contratos
from rentas import Rentas

class Welcome:
    def __init__(self):
        self.welcome()
    
    def welcome(self):
        root=tk.Tk()
        root.title("Bienvenido")
        root.geometry('690x630')
        root.resizable(False,False)

        
        #CENTRAR VENTANA
        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = root.winfo_screenwidth()
        htotal = root.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 690
        hventana = 630

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

        

        #Ver Historial de renta
        def load_data():
            for row in listaRentas.get_children():
                listaRentas.delete(row)
            conn=sqlite3.connect("adminCasa.db")
            cur=conn.cursor()
            cur.execute("SELECT * FROM Rentas")
            rows=cur.fetchall()
            for row in rows:
                listaRentas.insert("",tk.END,values=row)
            conn.close()
            update_ganancias()

        #Ver Inquilinos
        def view_inquilinos():  
            Inquilinos()

        #Ver Propiedades
        def view_propiedades():
            Propiedades()

        #Contratos
        def view_contratos():
            Contratos()

        def view_rentas():
            Rentas()

        def search_property():
            search_term = search_text.get()
            for row in listaRentas.get_children():
                listaRentas.delete(row)
            conn = sqlite3.connect("adminCasa.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM Rentas")
            rows = cur.fetchall()
            conn.close()
            try:
                for row in rows:
                    if search_term in row[1] or search_term in row[2] or search_term in row[4]:
                        listaRentas.insert("",tk.END,values=row)
            except:
                messagebox.showwarning("Advertencia", "No se encontro resultados.")
            update_ganancias()
            

        # Función para actualizar el label de ganancias
        def update_ganancias():
            total = 0
            for child in listaRentas.get_children():
                total += float(listaRentas.item(child)["values"][3])
            ganancias.config(text=f"${total:,.2f}")


        frame = tk.Frame(root, bg='#26c6da')
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        #Campo Buscar
        search_text = tk.StringVar()
        tk.Entry(frame, textvariable=search_text, bd=2, relief='sunken',font="Arial").grid(row=3, column=0, padx=10, pady=5, sticky='ew')
        tk.Button(frame, text="Buscar", bg='#2196F3', fg='white',font="Arial",command=search_property).grid(row=3, column=1, padx=5, pady=5, sticky='w')
        tk.Button(frame, text=" ⟳" , bg='#2196F3', fg='white',font="Arial",command=load_data).grid(row=3, column=2, padx=5, pady=5, sticky='w')


        #Botones
        tk.Button(frame, text="Inquilinos",bg='#4CAF50',command=view_inquilinos, fg='white',font="Arial").grid(row=5, column=0, padx=5, pady=5, sticky='ew')
        tk.Button(frame, text="Rentas",command=view_rentas,bg='#2196F3', fg='white',font="Arial").grid(row=6, column=1, padx=5, pady=5, sticky='ew')
        tk.Button(frame, text="Propiedades",bg='#FFC107',command=view_propiedades, fg='black',font="Arial").grid(row=6, column=0, padx=5, pady=5, sticky='ew')
        tk.Button(frame, text="Contratos",bg='#F44336',command=view_contratos, fg='white',font="Arial").grid(row=5, column=1, padx=5, pady=5, sticky='ew')
    
         # Treeview

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        columns = ("id_renta","nombre","direccion","renta","fecha")
        listaRentas = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        listaRentas.heading("id_renta", text="ID")
        listaRentas.heading("nombre", text="Nombre")
        listaRentas.heading("direccion", text="Direccion")
        listaRentas.heading("renta", text="Renta Mes")
        listaRentas.heading("fecha", text="Fecha")


        listaRentas.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

        # Especifica el ancho de cada columna
        listaRentas.column("id_renta", width=50)
        listaRentas.column("nombre", width=150)
        listaRentas.column("direccion", width=150)
        listaRentas.column("renta", width=100)
        listaRentas.column("fecha", width=130)

        # Scrollbar
        sb = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listaRentas.yview)
        sb.grid(row=7, column=3, sticky='ns')

        listaRentas.configure(yscrollcommand=sb.set)

        # Ganancias
        tk.Label(frame, text="Total", bg='#4CAF50',font="Arial").grid(row=8, column=2, padx=5, pady=5, sticky='nsew')
        ganancias = tk.Label(frame, text='$$$$$', bg='yellow',font="Arial")
        ganancias.grid(row=9, column=2, padx=5, pady=5, sticky='nsew')


        load_data()

        root.mainloop()
