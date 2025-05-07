from flask import Flask, render_template

app = Flask(__name__)

# Ruta para pag de inicio (movimientos)
@app.route('/')
def index():
    return render_template('index.html')

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