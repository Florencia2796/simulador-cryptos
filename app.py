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

        headers = {
            'x-cg-demo-api-key': api_key
        }

        try:
            if from_moneda == 'eur':
                # Compra de cripto con euros
                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {'ids': id_to, 'vs_currencies': 'eur'}
                response = requests.get(url, params=params, headers=headers).json()
                tasa = response[id_to]['eur']
                cantidad_to = cantidad_from / tasa

            elif to_moneda == 'eur':
                # Venta de cripto a euros
                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {'ids': id_from, 'vs_currencies': 'eur'}
                response = requests.get(url, params=params, headers=headers).json()
                tasa = response[id_from]['eur']
                cantidad_to = cantidad_from * tasa

            else:
                # Cripto a cripto: calcular usando EUR como moneda intermedia
                url = "https://api.coingecko.com/api/v3/simple/price"
                params = {
                    'ids': f'{id_from},{id_to}',
                    'vs_currencies': 'eur'
                }
                response = requests.get(url, params=params, headers=headers).json()
                tasa_from = response[id_from]['eur']
                tasa_to = response[id_to]['eur']
                tasa = tasa_from / tasa_to
                cantidad_to = cantidad_from * tasa

            resultado = {
                'from': from_moneda.upper(),
                'to': to_moneda.upper(),
                'cantidad_from': cantidad_from,
                'cantidad_to': round(cantidad_to, 8),
                'rate': round(tasa, 6)
            }

            datos_formulario = request.form

        except Exception as e:
            print("Error al calcular:", e)
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

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT from_moneda, cantidad_from, to_moneda, cantidad_to FROM movimientos")
    movimientos = cursor.fetchall()
    conn.close()

    euros_invertidos = 0
    euros_recuperados = 0
    cartera = {}

    for from_m, cant_from, to_m, cant_to in movimientos:
        if from_m == 'EUR':
            euros_invertidos += cant_from
        if to_m == 'EUR':
            euros_recuperados += cant_to

        if from_m != 'EUR':
            cartera[from_m] = cartera.get(from_m, 0) - cant_from
        if to_m != 'EUR':
            cartera[to_m] = cartera.get(to_m, 0) + cant_to

    saldo_euros = euros_invertidos - euros_recuperados

    # Obtener cotizaciones y valor actual de cada cripto
    valor_total = 0
    cotizaciones = {}
    headers = {'x-cg-demo-api-key': api_key}

    for cripto, cantidad in cartera.items():
        if cantidad <= 0:
            continue

        id_cripto = equivalencias.get(cripto.lower(), cripto.lower())

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {'ids': id_cripto, 'vs_currencies': 'eur'}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            try:
                precio = data[id_cripto]['eur']
                valor = cantidad * precio
                cotizaciones[cripto] = {
                    'cantidad': round(cantidad, 8),
                    'precio': round(precio, 6),
                    'valor_total': round(valor, 2)
                }
                valor_total += valor
            except KeyError:
                continue

    diferencia = round((valor_total + euros_recuperados) - euros_invertidos, 2)

    return render_template(
        "status.html",
        euros_invertidos=round(euros_invertidos, 2),
        euros_recuperados=round(euros_recuperados, 2),
        saldo_euros=round(saldo_euros, 2),
        valor_actual=round(valor_total, 2),
        diferencia=diferencia,
        cotizaciones=cotizaciones
    )

if __name__ == '__main__':
    app.run(debug=True)