import sqlite3

def agregar_datos_de_prueba():
    conn = sqlite3.connect('predio_logistico.db')
    c = conn.cursor()

    # Datos de prueba para la tabla de conductores
    conductores = [
        ('Juan Pérez', '12345678', 'ABC123'),
        ('María López', '87654321', 'XYZ789'),
        ('Carlos Gómez', '23456789', 'JKL456'),
        ('Ana Martínez', '98765432', 'QWE852'),
        ('Luis Torres', '45678912', 'MNB963')
    ]

    for conductor in conductores:
        nombre, dni, placa = conductor
        # Verificar si el conductor ya existe en la base de datos
        c.execute("SELECT id FROM conductores WHERE dni = ?", (dni,))
        if c.fetchone() is None:
            # Insertar conductor si no existe
            c.execute("INSERT INTO conductores (nombre, dni, placa) VALUES (?, ?, ?)", (nombre, dni, placa))

    conn.commit()
    print("Datos de prueba agregados o existentes preservados.")

    # Obtener IDs de los conductores insertados o existentes
    c.execute("SELECT id FROM conductores")
    ids_conductores = [row[0] for row in c.fetchall()]

    # Asignar ubicaciones de prueba para cada conductor
    ubicaciones = [
        (ids_conductores[0], 'vigilancia'),
        (ids_conductores[1], 'playa de espera'),
        (ids_conductores[2], 'dock 1'),
        (ids_conductores[3], 'dock 2'),
        (ids_conductores[4], 'dock 3')
    ]

    # Eliminar ubicaciones anteriores antes de insertar nuevas ubicaciones de prueba
    c.execute("DELETE FROM ubicaciones")
    c.executemany("INSERT INTO ubicaciones (id_conductor, ubicacion) VALUES (?, ?)", ubicaciones)
    
    conn.commit()
    conn.close()
    print("Ubicaciones iniciales agregadas o actualizadas con éxito.")

if __name__ == '__main__':
    agregar_datos_de_prueba()
