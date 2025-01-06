import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk

class Propiedades:
    def __init__(self):
        self.propiedades()
    
    def propiedades(self):
        root=tk.Toplevel()
        root.title("Mis propiedades")
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

        

        def load_data():
            for row in listaPropiedades.get_children():
                listaPropiedades.delete(row)
            conn = sqlite3.connect("adminCasa.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM Propiedades")
            rows = cur.fetchall()
            for row in rows:
                # Convertir el valor de la columna 3
                rent_status = "Rentada" if row[3] == 1 else "No Rentada"
                # Crear una nueva tupla con el valor convertido
                new_row = (row[0], row[1], row[2], rent_status) + row[4:]
                listaPropiedades.insert("", tk.END, values=new_row)
            conn.close()

        #ADD Propieadades
        def add_propieadad():
            direccion = direccion_entry.get()
            renta_mensual = renta_mensual_entry.get()
            esta_rentada = esta_rentada_box_value.get()
            conn = sqlite3.connect("adminCasa.db")
            cursor = conn.cursor()   
            if direccion and renta_mensual:
                cursor.execute("INSERT INTO Propiedades (direccion, renta_mensual, esta_rentada) VALUES (?, ?, ?)",
                                    (direccion, renta_mensual, esta_rentada))
                conn.commit()
                load_data()
                clear_entries()
                print("Se agrego correctamente")
            else:
                messagebox.showwarning("Advertencia", "Llena los campos")
            conn.close()
        #ACTUALIZAR INQUILINOS
        def update_propieadad():
            try:
                selected_item = listaPropiedades.focus()
                item_id = listaPropiedades.item(selected_item, 'values')[0]

                direccion = direccion_entry.get()
                renta_mensual = renta_mensual_entry.get()
                esta_rentada = esta_rentada_box_value.get()
                conn = sqlite3.connect("adminCasa.db")
                cursor = conn.cursor()   

                if direccion and renta_mensual:
                    cursor.execute("UPDATE Propiedades SET direccion=?, renta_mensual=?, esta_rentada=? WHERE id_propiedad=?",
                                    (direccion, renta_mensual, esta_rentada, item_id))
                    conn.commit()
                    load_data()
                    clear_entries()
                    print("Se Actualizo correctamente")

                else:
                    messagebox.showwarning("Advertencia", "Llena los campos.")
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un inquilino para actualizar.")
                
        #ELIMINAR INQUILINOS
        def delete_propiedad():
            try:
                selected_item=listaPropiedades.focus()
                item_id=listaPropiedades.item(selected_item, 'values')[0]
                conn=sqlite3.connect("adminCasa.db")
                cursor=conn.cursor()
                cursor.execute("DELETE FROM Propiedades WHERE id_propiedad=?", (item_id,))
                conn.commit()
                load_data()
                clear_entries()
                print("Se Elimino correctamente")
                conn.close()
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona una propiedad para Eliminar.")
        #SELECCIONAR   
        def get_selected_row(event):
            try:
                selected_item = listaPropiedades.focus()
                item = listaPropiedades.item(selected_item, 'values')
                direccion_entry.delete(0, tk.END)
                direccion_entry.insert(tk.END, item[1])
                renta_mensual_entry.delete(0, tk.END)
                renta_mensual_entry.insert(tk.END, item[2])
                if item[3]=="Rentada":
                    esta_rentada_box_value.set(True)
                else:
                    esta_rentada_box_value.set(False)
            except IndexError:
                pass

        def clear_entries():
            direccion_entry.delete(0, tk.END)
            renta_mensual_entry.delete(0, tk.END)
            esta_rentada_box_value.set(False)

        def __del__():
            conn.close()

        def only_numbers(char):
            return char.isdigit()
        
        validate_command = (root.register(only_numbers), '%S')

#WIDGETS
        frame = tk.Frame(root, bg='#76acb3')
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        direccion_label = tk.Label(frame, text="Direccion:",font="Arial", bg='#76acb3')
        direccion_label.grid(row=0, column=0, padx=10, pady=10)
        direccion_entry = tk.Entry(frame,font="Arial")
        direccion_entry.grid(row=0, column=1, padx=10, pady=10)

        renta_mensual_label = tk.Label(frame, text="Renta mensual:",font="Arial", bg='#76acb3')
        renta_mensual_label.grid(row=1, column=0, padx=10, pady=10)
        renta_mensual_entry = tk.Entry(frame,font="Arial",validate="key", validatecommand=validate_command)
        renta_mensual_entry.grid(row=1, column=1, padx=10, pady=10)

        esta_rentada_label = tk.Label(frame, text="Esta rentada?:",font="Arial", bg='#76acb3')
        esta_rentada_label.grid(row=0, column=2, padx=10, pady=10)
        esta_rentada_box_value=tk.BooleanVar()
        esta_rentada_box = tk.Checkbutton(frame,variable=esta_rentada_box_value, bg='#76acb3')
        esta_rentada_box.grid(row=1, column=2,padx=10, pady=10)

        add_button = tk.Button(frame, text="Agregar", command=add_propieadad,bg='#4CAF50', fg='white',font="Arial")
        add_button.grid(row=3, column=0, padx=10, pady=10,sticky='ew')
        update_button = tk.Button(frame, text="Actualizar", command=update_propieadad,bg='#FFC107', fg='white',font="Arial")
        update_button.grid(row=3, column=1, padx=10, pady=10,sticky='ew')
        delete_button = tk.Button(frame, text="Eliminar", command=delete_propiedad,bg='#F44336', fg='white',font="Arial")
        delete_button.grid(row=3, column=2, padx=10, pady=10,sticky='ew')


 # Treeview

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        columns = ("id_propiedad", "direccion", "renta_mensual", "esta_rentada")
        listaPropiedades = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        listaPropiedades.heading("id_propiedad", text="ID")
        listaPropiedades.heading("direccion", text="Direccion")
        listaPropiedades.heading("renta_mensual", text="Renta")
        listaPropiedades.heading("esta_rentada", text="Estado")
        listaPropiedades.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Especifica el ancho de cada columna
        listaPropiedades.column("id_propiedad", width=50)
        listaPropiedades.column("direccion", width=300)
        listaPropiedades.column("renta_mensual", width=170)
        listaPropiedades.column("esta_rentada", width=90)

        # Scrollbar
        sb = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listaPropiedades.yview)
        sb.grid(row=5, column=3, sticky='ns')
        listaPropiedades.configure(yscrollcommand=sb.set)

        listaPropiedades.bind("<<TreeviewSelect>>", get_selected_row)

        load_data()




        root.mainloop()