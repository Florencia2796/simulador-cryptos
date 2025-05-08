from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("COINAPI_KEY")
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'database.db')

app = Flask(__name__)

MONEDAS = ["EUR", "BTC", "ETH", "USDT", "ADA", "SOL", "XRP", "DOT", "DOGE", "SHIB"]

@app.route('/')
def index():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    conn.close()
    return render_template("index.html", movimientos=movimientos)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    resultado = None
    datos_formulario = {}

    if request.method == 'POST' and 'calcular' in request.form:
        try:
            from_moneda = request.form['from']
            to_moneda = request.form['to']
            cantidad_from = float(request.form['cantidad'])

            url = f"https://rest.coinapi.io/v1/exchangerate/{from_moneda}/{to_moneda}"
            headers = {'X-CoinAPI-Key': API_KEY}
            response = requests.get(url, headers=headers).json()

            if 'rate' in response:
                rate = response['rate']
                cantidad_to = cantidad_from * rate

                resultado = {
                    'from': from_moneda,
                    'to': to_moneda,
                    'cantidad_from': cantidad_from,
                    'cantidad_to': round(cantidad_to, 8),
                    'rate': round(rate, 4)
                }

                datos_formulario = request.form
            else:
                resultado = None
        except Exception as e:
            resultado = None

    elif request.method == 'POST' and 'confirmar' in request.form:
        try:
            from_moneda = request.form['from']
            to_moneda = request.form['to']
            cantidad_from = float(request.form['cantidad_from'])
            cantidad_to = float(request.form['cantidad_to'])
            rate = float(request.form['rate'])

            fecha = datetime.now().strftime('%d/%m/%Y')
            hora = datetime.now().strftime('%H:%M:%S')

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO movimientos (fecha, hora, from_moneda, cantidad_from, to_moneda, cantidad_to, valor_unitario)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (fecha, hora, from_moneda, cantidad_from, to_moneda, cantidad_to, rate))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

        except Exception as e:
            return redirect(url_for('purchase'))

    return render_template(
        "purchase.html",
        monedas=MONEDAS,
        resultado=resultado,
        from_moneda=datos_formulario.get('from'),
        to_moneda=datos_formulario.get('to'),
        cantidad=datos_formulario.get('cantidad', '')
    )

@app.route('/status')
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True)
