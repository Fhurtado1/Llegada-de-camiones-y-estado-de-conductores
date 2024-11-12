# setup_database.py

import sqlite3

def setup_database():
    conn = sqlite3.connect('predio_logistico.db')
    c = conn.cursor()

    # Crear tabla de conductores
    c.execute('''
        CREATE TABLE IF NOT EXISTS conductores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            dni TEXT UNIQUE,
            placa TEXT
        )
    ''')

    # Crear tabla de ubicaciones
    c.execute('''
        CREATE TABLE IF NOT EXISTS ubicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_conductor INTEGER,
            ubicacion TEXT,
            hora_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hora_salida TIMESTAMP,
            FOREIGN KEY(id_conductor) REFERENCES conductores(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
