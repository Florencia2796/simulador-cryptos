from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COINAPI_KEY")
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
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        from_moneda = request.form['from']
        to_moneda = request.form['to']
        cantidad_from = float(request.form['cantidad'])

        # Llamada a CoinAPI para obtener el valor unitario
        url = f"https://rest.coinapi.io/v1/exchangerate/{from_moneda}/{to_moneda}"
        headers = {'X-CoinAPI-Key': API_KEY}
        response = requests.get(url, headers=headers).json()

        rate = response['rate']
        cantidad_to = cantidad_from * rate

        # Fecha y hora actuales
        fecha = datetime.now().strftime('%d/%m/%Y')
        hora = datetime.now().strftime('%H:%M:%S')

        # Guardar en la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movimientos (fecha, hora, from_moneda, cantidad_from, to_moneda, cantidad_to, valor_unitario)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fecha, hora, from_moneda, cantidad_from, to_moneda, cantidad_to, rate))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('purchase.html')

# Ruta para pag de estado de la inversión
@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True)