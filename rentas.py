import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class Rentas:
    def __init__(self):
        self.rentas()
    
    def rentas(self):
        root=tk.Toplevel()
        root.title("Rentas")
        root.geometry('700x700')
        root.resizable(False,False)
        root.grab_set()

        
        #CENTRAR VENTANA
        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = root.winfo_screenwidth()
        htotal = root.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 700
        hventana = 700

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

        #VER LOS DATOS
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

            menu_propiedades()

            #MENU PROPIEDADES
        def menu_propiedades():
            conn = sqlite3.connect("adminCasa.db")
            cur = conn.cursor()
            cur.execute("SELECT direccion FROM Propiedades")
            rows = cur.fetchall()  # Obtener todas las filas
            conn.close()

            info_list = []
            if rows:
                    info_list = [row[0] for row in rows]  # Extraer solo las direcciones 
                    print(info_list)
            else:
                messagebox.showwarning("Advertencia", "No se encontraron Propiedades.")

            propiedad_menu['values'] = info_list
            propiedad_menu.set('')
        
        #LLenar VALORES
        def ver_valores():
            propiedad = propiedad_menu.get()
            conn = sqlite3.connect("adminCasa.db")
            cursor = conn.cursor()
            #RentaMensual
            cursor.execute("SELECT renta_mensual FROM Contratos WHERE direccion=?", (propiedad,))
            resultado_renta = cursor.fetchone() # Obtén el primer resultado
            renta_mensual = resultado_renta[0] if resultado_renta else None
            renta_entry.delete(0, tk.END)
            renta_entry.insert(tk.END, str(renta_mensual))            
        
            #Nombre
            cursor.execute("SELECT nombre FROM Contratos WHERE direccion=?", (propiedad,))
            resultado_nombre = cursor.fetchone() # Obtén el primer resultado
            nombre = resultado_nombre[0] if resultado_nombre else None
            nombre_entry.delete(0, tk.END)
            nombre_entry.insert(tk.END, str(nombre))

        #Limpiar campos
        def clear_entries():
            propiedad_menu.set("")
            nombre_entry.delete(0,tk.END)
            renta_entry.delete(0, tk.END)
            fecha_calendar.set_date(datetime.today())


        def add_renta():
             propiedad = propiedad_menu.get()
             nombre=nombre_entry.get()
             renta = renta_entry.get()
             fecha = fecha_calendar.get_date()

             conn = sqlite3.connect("adminCasa.db")
             cursor = conn.cursor()
             if nombre and propiedad and renta and fecha:
                if nombre=="None" or renta=="None":
                    messagebox.showwarning("Advertencia", "LLene los datos correctamente")

                else:
                    cursor.execute("""
                        INSERT INTO Rentas (nombre, direccion, renta, fecha)
                        VALUES (?, ?, ?, ?)
                        """, (nombre,propiedad, renta, fecha))
                    conn.commit()
                    load_data()
                    clear_entries()
                    conn.close()
                    print("Se agregó correctamente")
             else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

        #Eliminar contrato
        def delete_renta():
            try:
                selected_item = listaRentas.focus()
                item_id = listaRentas.item(selected_item, 'values')[0]
                conn = sqlite3.connect("adminCasa.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Rentas WHERE id_renta=?", (item_id,))
                conn.commit()
                load_data()
                clear_entries()
                conn.close()
                print("Se eliminó correctamente")
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un contrato para eliminar.")

        #Seleccionar linea
        def get_selected_row(event):
            try:
                selected_item = listaRentas.focus()
                item = listaRentas.item(selected_item, 'values')
                propiedad_menu.set(item[2])
                nombre_entry.delete(0, tk.END)
                nombre_entry.insert(tk.END, item[1])
                renta_entry.delete(0, tk.END)
                renta_entry.insert(tk.END, item[3])
                #HAY QUE PASAR LA FECHA EN FORMATO CORRECTO 
                fecha_calendar.set_date(datetime.strptime(item[4], '%Y-%m-%d').date())
            except IndexError:
                pass


        def only_numbers(char):
            return char.isdigit()
        
        validate_command = (root.register(only_numbers), '%S')

        #Frame1
        frame1=tk.Frame(root, bg='#76acb3')
        frame1.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        #Menu
        propiedad_label=tk.Label(frame1, text="Propiedad: ",font="Arial", bg='#76acb3').grid(row=1,column=0)
        propiedad_menu=ttk.Combobox(frame1,state="readonly",font="Arial")
        propiedad_menu.grid(row=1, column=1, padx=5, pady=10)
        propiedad_menu.bind('<<ComboboxSelected>>', lambda event: ver_valores())

        #Entrys
        nombre_label=tk.Label(frame1,text="Inquilino: ",font="Arial", bg='#76acb3')
        nombre_label.grid(row=2,column=0,padx=5,pady=10)
        nombre_entry=tk.Entry(frame1,font="Arial")
        nombre_entry.grid(row=2,column=1, padx=5, pady=10)

        renta_label=tk.Label(frame1,text="Renta $",font="Arial", bg='#76acb3')
        renta_label.grid(row=3,column=0,padx=5,pady=10)
        renta_entry=tk.Entry(frame1,font="Arial",validate="key", validatecommand=validate_command)
        renta_entry.grid(row=3,column=1, padx=5, pady=10)


        #Fechas
        fecha_label=tk.Label(frame1, text="Fecha: ",font="Arial", bg='#76acb3').grid(row=4,column=0)
        fecha_calendar=DateEntry(frame1,locale='es_ES',date_pattern='dd-mm-y',font="Arial")
        fecha_calendar.grid(row=4,column=1)

        #Botones
        nuevo_button=tk.Button(frame1, text="Nuevo",bg='#4CAF50',fg='white',font="Arial",command=add_renta).grid(row=5, column=0, padx=5, pady=5, sticky='ew')
        update_button=tk.Button(frame1, text="---------- ",bg='#2196F3', fg='white',font="Arial").grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        delete_button=tk.Button(frame1, text="Eliminar",bg='#F44336', fg='black',font="Arial",command=delete_renta).grid(row=5, column=2, padx=5, pady=5, sticky='ew')

         # Treeview

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        columns = ("id_renta","nombre","direccion","renta","fecha")
        listaRentas = ttk.Treeview(frame1, columns=columns, show='headings', height=15)
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
        sb = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=listaRentas.yview)
        sb.grid(row=7, column=3, sticky='ns')

        listaRentas.configure(yscrollcommand=sb.set)
        listaRentas.bind("<<TreeviewSelect>>", get_selected_row)


        load_data()

        root.mainloop()



        
