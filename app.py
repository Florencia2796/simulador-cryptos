import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)

# Ruta a la base
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')

@app.route('/')
def index():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    conn.close()
    return render_template("index.html", movimientos=movimientos)

# Ruta para pag de cambio
@app.route('/purchase')
def purchase():
    return render_template('purchase.html')

# Ruta para pag de estado de la inversión
@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True)