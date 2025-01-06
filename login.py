import tkinter as tk
from tkinter import messagebox
import sqlite3
from welcome import Welcome


class Login:
    def __init__(self):
        self.login()
    
    def login(self):
        root=tk.Tk()
        root.title("Login")
        root.geometry('400x500')
        root.resizable(False,False)

        #CENTRAR VENTANA
        #  Obtenemos el largo y  ancho de la pantalla
        wtotal = root.winfo_screenwidth()
        htotal = root.winfo_screenheight()
        #  Guardamos el largo y alto de la ventana
        wventana = 400
        hventana = 500

        #  Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal/2-wventana/2)
        pheight = round(htotal/2-hventana/2)

        #  Se lo aplicamos a la geometría de la ventana
        root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

        
        entry_username = tk.StringVar()
        entry_password = tk.StringVar()

        def entrar():
            username = entry_username.get()
            password = entry_password.get()
            if validar(username, password):
                print("Se valido correctamente")
                root.destroy()
                Welcome()
            else:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")       

        def validar(usuario, password):
            conn = sqlite3.connect('adminCasa.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (usuario, password))
            user = c.fetchone()
            conn.close()
            return user is not None


        #Frame
        frame=tk.Frame(root, bg='#76acb3')
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        #LabelUsuario
        tk.Label(frame,text='Usuario',font="Arial", bg='#76acb3').pack(pady=5)
        tk.Entry(frame,textvariable=entry_username,font="Arial").pack(pady=5)
        #LabelPassword
        tk.Label(frame,text='Password',font="Arial", bg='#76acb3').pack(pady=5)
        tk.Entry(frame,textvariable=entry_password,show="*",font="Arial").pack(pady=5)

        # Botón de inicio de sesión
        tk.Button(frame, text="Iniciar",command=entrar, bg='#2196F3', fg='white',font="Arial").pack(pady=20)

        root.mainloop()
