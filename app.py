from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
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

    # CoinGecko usa estos IDs en vez de BTC, ETH, etc.
    equivalencias = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'usdt': 'tether',
        'ada': 'cardano',
        'sol': 'solana',
        'xrp': 'ripple',
        'dot': 'polkadot',
        'doge': 'dogecoin',
        'shib': 'shiba-inu',
        'eur': 'eur'
    }

    api_key = os.getenv("COINGECKO_API_KEY")

    if request.method == 'POST' and 'calcular' in request.form:
        from_moneda = request.form['from'].lower()
        to_moneda = request.form['to'].lower()
        cantidad_from = float(request.form['cantidad'])

        id_from = equivalencias.get(from_moneda, from_moneda)
        id_to = equivalencias.get(to_moneda, to_moneda)

        # Si la moneda de origen es EUR, invertimos la lógica
        if id_from == 'eur':
            ids = id_to
            vs_currencies = id_from
            inversion = True
        else:
            ids = id_from
            vs_currencies = id_to
            inversion = False

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ids,
            'vs_currencies': vs_currencies
        }

        headers = {
            'x-cg-demo-api-key': api_key
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            resultado = None  # podrías manejar el error más explícitamente
        else:
            data = response.json()

            try:
                tasa = data[ids][vs_currencies]
                if inversion:
                    cantidad_to = cantidad_from / tasa
                else:
                    cantidad_to = cantidad_from * tasa

                resultado = {
                    'from': from_moneda.upper(),
                    'to': to_moneda.upper(),
                    'cantidad_from': cantidad_from,
                    'cantidad_to': round(cantidad_to, 8),
                    'rate': round(tasa, 6)
                }

                datos_formulario = request.form

            except KeyError:
                resultado = None

    elif request.method == 'POST' and 'confirmar' in request.form:
        from_moneda = request.form['from']
        to_moneda = request.form['to']
        cantidad_from = float(request.form['cantidad'])
        rate = request.form.get('rate')
        if not rate:
            return redirect(url_for('purchase'))
        rate = float(rate)
        cantidad_to = cantidad_from * rate

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