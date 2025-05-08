import sqlite3
import os

# Ruta a la base de datos dentro de 'instance/'
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')

# Conexión
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear tabla de movimientos
cursor.execute('''
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    hora TEXT,
    from_moneda TEXT,
    cantidad_from REAL,
    to_moneda TEXT,
    cantidad_to REAL,
    valor_unitario REAL
)
''')

conn.commit()
conn.close()

print("Base de datos creada correctamente.")
