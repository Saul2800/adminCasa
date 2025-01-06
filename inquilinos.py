import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk

class Inquilinos:
    def __init__(self):
        self.inquilinos()
    
    def inquilinos(self):
        root=tk.Toplevel()
        root.title("Inquilinos")
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
            for row in tree.get_children():
                tree.delete(row)
            conn = sqlite3.connect("adminCasa.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM inquilinos")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
            conn.close()

        #ADD INQUILINOS
        def add_inquilino():
            nombre = nombre_entry.get()
            apellido = apellido_entry.get()
            telefono = telefono_entry.get()
            conn = sqlite3.connect("adminCasa.db")
            cursor = conn.cursor()   
            if nombre and apellido and telefono:
                cursor.execute("INSERT INTO inquilinos (nombre, apellido, telefono) VALUES (?, ?, ?)",
                                    (nombre, apellido, telefono))
                conn.commit()
                load_data()
                clear_entries()
                print("Se agregó correctamente")
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            conn.close()

        #ACTUALIZAR INQUILINOS
        def update_inquilino():
            try:
                selected_item = tree.focus()
                item_id = tree.item(selected_item, 'values')[0]

                nombre = nombre_entry.get()
                apellido = apellido_entry.get()
                telefono = telefono_entry.get()
                conn = sqlite3.connect("adminCasa.db")
                cursor = conn.cursor()   

                if nombre and apellido and telefono:
                    cursor.execute("UPDATE inquilinos SET nombre=?, apellido=?, telefono=? WHERE id_inquilino=?",
                                    (nombre, apellido, telefono, item_id))
                    conn.commit()
                    load_data()
                    clear_entries()
                    print("Se actualizó correctamente")
                else:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                conn.close()
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un inquilino para actualizar.")

                
        #ELIMINAR INQUILINOS
        def delete_inquilino():
            try:
                selected_item = tree.focus()
                item_id = tree.item(selected_item, 'values')[0]
                conn = sqlite3.connect("adminCasa.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inquilinos WHERE id_inquilino=?", (item_id,))
                conn.commit()
                load_data()
                clear_entries()
                print("Se eliminó correctamente")
                conn.close()
            except IndexError:
                messagebox.showwarning("Advertencia", "Selecciona un inquilino para eliminar.")
        #SELECCIONAR   

        def get_selected_row(event):
            try:
                selected_item = tree.focus()
                item = tree.item(selected_item, 'values')
                nombre_entry.delete(0, tk.END)
                nombre_entry.insert(tk.END, item[1])
                apellido_entry.delete(0, tk.END)
                apellido_entry.insert(tk.END, item[2])
                telefono_entry.delete(0, tk.END)
                telefono_entry.insert(tk.END, item[3])
            except IndexError:
                pass

        def clear_entries():
            nombre_entry.delete(0, tk.END)
            apellido_entry.delete(0, tk.END)
            telefono_entry.delete(0, tk.END)

        def __del__():
            conn.close()

        def only_numbers(char):
            return char.isdigit()
        
        validate_command = (root.register(only_numbers), '%S')

#WIDGETS
        frame = tk.Frame(root, bg='#76acb3')
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)


        nombre_label = tk.Label(frame, text="Nombre:",font="Arial", bg='#76acb3')
        nombre_label.grid(row=0, column=0, padx=10, pady=10)
        nombre_entry = tk.Entry(frame,font="Arial")
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)

        apellido_label = tk.Label(frame, text="Apellido:",font="Arial", bg='#76acb3')
        apellido_label.grid(row=1, column=0, padx=10, pady=10)
        apellido_entry = tk.Entry(frame,font="Arial")
        apellido_entry.grid(row=1, column=1, padx=10, pady=10)

        telefono_label = tk.Label(frame, text="Teléfono:",font="Arial", bg='#76acb3')
        telefono_label.grid(row=2, column=0, padx=10, pady=10)
        telefono_entry = tk.Entry(frame,font="Arial",validate="key", validatecommand=validate_command)
        telefono_entry.grid(row=2, column=1, padx=10, pady=10)

        add_button = tk.Button(frame, text="Agregar", command=add_inquilino,font="Arial",bg='#4CAF50')
        add_button.grid(row=3, column=0, padx=10, pady=10,sticky='ew')
        update_button = tk.Button(frame, text="Actualizar", command=update_inquilino,font="Arial",bg='#2196F3')
        update_button.grid(row=3, column=1, padx=10, pady=10,sticky='ew')
        delete_button = tk.Button(frame, text="Eliminar", command=delete_inquilino,font="Arial",bg='#F44336')
        delete_button.grid(row=3, column=2, padx=10, pady=10,sticky='ew')

        # Treeview

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 12),)

        columns = ("id_inquilino", "nombre", "apellido", "telefono")
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        tree.heading("id_inquilino", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("apellido", text="Apellido")
        tree.heading("telefono", text="Teléfono")
        tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Especifica el ancho de cada columna
        tree.column("id_inquilino", width=50)
        tree.column("nombre", width=150)
        tree.column("apellido", width=200)
        tree.column("telefono", width=200)

        # Scrollbar
        sb = tk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        sb.grid(row=5, column=3, sticky='ns')
        tree.configure(yscrollcommand=sb.set)

        tree.bind("<<TreeviewSelect>>", get_selected_row)

        load_data()




        root.mainloop()