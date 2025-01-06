import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class Contratos:
    def __init__(self):
        self.contratos()
    
    def contratos(self):
        root=tk.Toplevel()
        root.title("Contratos")
        root.geometry('900x700')
        root.resizable(False,False)
        root.grab_set()

        
        #CENTRAR VENTANA
        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = root.winfo_screenwidth()
        htotal = root.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 900
        hventana = 700

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

        #VER LOS DATOS
        def load_data():
            for row in listaContratos.get_children():
                listaContratos.delete(row)
            conn=sqlite3.connect("adminCasa.db")
            cur=conn.cursor()
            cur.execute("SELECT * FROM Contratos")
            rows=cur.fetchall()
            for row in rows:
                listaContratos.insert("",tk.END,values=row)
            conn.close()

            menu_inquilinos()
            menu_propiedades()

            #Menu inquilinos
        def menu_inquilinos():
            conn = sqlite3.connect("adminCasa.db")
            cur = conn.cursor()
            cur.execute("SELECT id_inquilino, nombre FROM Inquilinos")
            rows = cur.fetchall()  # Obtener todas las filas
            conn.close()

            info_list = []
            if rows:
                    info_list = [f"{row[0]} - {row[1]}" for row in rows]  # Concatenar ID y nombre
                    print(info_list)
            else:
                messagebox.showwarning("Advertencia", "No se encontraron inquilinos.")

            inquilino_menu['values'] = info_list
            inquilino_menu.set('')
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
        
        
        #Añadir contrato
        def add_contrato():
            inquilino = inquilino_menu.get()
            propiedad = propiedad_menu.get()
            deposito = deposito_entry.get()
            fecha_inicio = fecha_inicio_calendar.get_date()
            fecha_fin = fecha_Fin_calendar.get_date()

            conn = sqlite3.connect("adminCasa.db")
            cursor = conn.cursor()
            cursor.execute("SELECT renta_mensual FROM Propiedades WHERE direccion=?", (propiedad,))
            resultado = cursor.fetchone() # Obtén el primer resultado
            renta_mensual = resultado[0] if resultado else None

            if inquilino and propiedad and deposito and fecha_inicio and fecha_fin:
                cursor.execute("""
                    INSERT INTO Contratos (nombre, direccion, renta_mensual, deposito_realizado, fecha_inicio,fecha_fin)
                    VALUES (?, ?, ?, ?, ?,?)
                    """, (inquilino, propiedad,renta_mensual, deposito, fecha_inicio, fecha_fin))
                conn.commit()
                load_data()
                clear_entries()
                conn.close()
                print("Se agregó correctamente")
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        
        #Actualizar contrato
        def update_contrato():
            try:
                selected_item = listaContratos.focus()
                item_id = listaContratos.item(selected_item, 'values')[0]

                id_inquilino = inquilino_menu.get()
                id_propiedad = propiedad_menu.get()
                deposito = deposito_entry.get()
                fecha_inicio = fecha_inicio_calendar.get_date()
                fecha_fin = fecha_Fin_calendar.get_date()

                conn = sqlite3.connect("adminCasa.db")
                cursor = conn.cursor()

                if id_inquilino and id_propiedad and deposito:
                    cursor.execute("""
                        UPDATE contratos 
                        SET id_inquilino=?, id_propiedad=?, deposito_realizado=?, fecha_inicio=?, fecha_fin=?
                        WHERE id_contrato=?
                        """, (id_inquilino, id_propiedad, deposito, fecha_inicio, fecha_fin, item_id))
                    conn.commit()
                    load_data()
                    clear_entries()
                    conn.close()
                    print("Se actualizó correctamente")
                else:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un contrato para actualizar.")


        #Eliminar contrato
        def delete_contrato():
            try:
                selected_item = listaContratos.focus()
                item_id = listaContratos.item(selected_item, 'values')[0]
                conn = sqlite3.connect("adminCasa.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Contratos WHERE id_contrato=?", (item_id,))
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
                selected_item = listaContratos.focus()
                item = listaContratos.item(selected_item, 'values')
                inquilino_menu.set(item[1])
                propiedad_menu.set(item[2])
                deposito_entry.delete(0, tk.END)
                deposito_entry.insert(tk.END, item[4])
                #HAY QUE PASAR LA FECHA EN FORMATO CORRECTO 
                fecha_inicio_calendar.set_date(datetime.strptime(item[5], '%Y-%m-%d').date())
                fecha_Fin_calendar.set_date(datetime.strptime(item[6], '%Y-%m-%d').date())
            except IndexError:
                pass

            
        #Limpiar campos
        def clear_entries():
            inquilino_menu.set("")
            propiedad_menu.set("")
            deposito_entry.delete(0, tk.END)
            fecha_inicio_calendar.set_date(datetime.today())
            fecha_Fin_calendar.set_date(datetime.today())

        def only_numbers(char):
            return char.isdigit()
        
        validate_command = (root.register(only_numbers), '%S')

        #Frame1
        frame1=tk.Frame(root, bg='#76acb3')
        frame1.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        #Botones

        #Menus
        inquilino_menu=ttk.Combobox(frame1,state="readonly",font="Arial")
        inquilino_menu.grid(row=7, column=0, padx=5, pady=10,sticky='w')
        propiedad_menu=ttk.Combobox(frame1,state="readonly",font="Arial")
        propiedad_menu.grid(row=7, column=1, padx=5, pady=10,sticky='w')

        #Entrys
        deposito_label=tk.Label(frame1,text="Deposito $",font="Arial", bg='#76acb3')
        deposito_label.grid(row=8,column=0,padx=5,pady=10,sticky='e')
        deposito_entry=tk.Entry(frame1,font="Arial",validate="key", validatecommand=validate_command)
        deposito_entry.grid(row=8,column=1, padx=5, pady=10,sticky='w')

        #Fechas
        fecha_inicio_label=tk.Label(frame1, text="Fecha de inicio",font="Arial", bg='#76acb3').grid(row=9,column=0,sticky='e')
        fecha_inicio_calendar=DateEntry(frame1,locale='es_ES',date_pattern='dd-mm-y',font="Arial")
        fecha_inicio_calendar.grid(row=9,column=1,sticky='w')
        fecha_Fin_label=tk.Label(frame1, text="Fecha de Fin",font="Arial", bg='#76acb3').grid(row=10,column=0,sticky='e')
        fecha_Fin_calendar=DateEntry(frame1,locale='es_ES',date_pattern='dd-mm-y',font="Arial")
        fecha_Fin_calendar.grid(row=10,column=1,sticky='w')

        nuevo_button=tk.Button(frame1, text="Nuevo",bg='#4CAF50',fg='white',font="Arial",command=add_contrato).grid(row=11, column=0, padx=5, pady=5, sticky='ew')
        update_button=tk.Button(frame1, text="---------- ",bg='#2196F3', fg='white',font="Arial").grid(row=11, column=1, padx=5, pady=5, sticky='ew')
        delete_button=tk.Button(frame1, text="Eliminar",bg='#F44336', fg='black',font="Arial",command=delete_contrato).grid(row=11, column=2, padx=5, pady=5, sticky='ew')


        # Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        columns = ("id_contrato","nombre","direccion","renta_mensual","deposito_realizado","fecha_inicio","fecha_fin")
        listaContratos = ttk.Treeview(frame1, columns=columns, show='headings', height=15)
        listaContratos.heading("id_contrato", text="ID")
        listaContratos.heading("nombre", text="Nombre")
        listaContratos.heading("direccion", text="Direccion")
        listaContratos.heading("renta_mensual", text="RentaXmes")
        listaContratos.heading("deposito_realizado", text="Deposito")
        listaContratos.heading("fecha_inicio", text="Inicio")
        listaContratos.heading("fecha_fin", text="Fin")


        listaContratos.grid(row=12, column=0, columnspan=3, padx=10, pady=10)

        # Especifica el ancho de cada columna
        listaContratos.column("id_contrato", width=50)
        listaContratos.column("nombre", width=150)
        listaContratos.column("direccion", width=150)
        listaContratos.column("renta_mensual", width=100)
        listaContratos.column("deposito_realizado", width=100)
        listaContratos.column("fecha_inicio", width=130)
        listaContratos.column("fecha_fin", width=130)


        # Scrollbar
        sb = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=listaContratos.yview)
        sb.grid(row=12, column=3, sticky='ns')
        listaContratos.configure(yscrollcommand=sb.set)
        listaContratos.bind("<<TreeviewSelect>>", get_selected_row)


        load_data()

        root.mainloop()



        
