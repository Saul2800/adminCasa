import sqlite3

def DB():
    # Conectar a la base de datos (o crearla si no existe)
    conn = sqlite3.connect('adminCasa.db')
    cursor = conn.cursor()

    #Crear la tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Verificar si la tabla está vacía
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    # Insertar el usuario y la contraseña si la tabla está vacía
    if count == 0:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', ('admin', 'admin'))


    # Crear la tabla de Inquilinos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inquilinos (
        id_inquilino INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono TEXT NOT NULL
    )
    ''')

    # Crear la tabla de Propiedades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Propiedades (
        id_propiedad INTEGER PRIMARY KEY,
        direccion TEXT NOT NULL,
        renta_mensual TEXT NOT NULL,
        esta_rentada INTEGER NOT NULL
    )
    ''')

    # Crear la tabla de Contratos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contratos (
        id_contrato INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        direccion TEXT NOT NULL,
        renta_mensual TEXT NOT NULL,
        deposito_realizado TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        fecha_fin TEXT NOT NULL
    )
    ''')

    # Crear la tabla de Rentas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rentas (
        id_renta INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        direccion TEXT NOT NULL,
        renta TEXT NOT NULL,
        fecha TEXT NOT NULL
    )
    ''')


    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
