from flask import Flask, request, render_template

MONEDAS = ("CLP", "AR", "CO", "MX", "PE", "USD")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    texto_conversion = None
    if request.method == 'POST':
        monto = request.form['monto']
        moneda_origen = request.form['moneda_origen']
        moneda_destino = request.form['moneda_destino']
        monto_destino = None

        if moneda_destino == 'USD' and moneda_origen == 'CLP':
            monto_destino = int(monto) / 800.0
        elif moneda_destino == 'CLP' and moneda_origen == 'USD':
            monto_destino = int(monto) * 800.0

        if monto_destino is None:
            texto_conversion = f"""
<div class="alert">Quieres convertir <strong>${monto} {moneda_origen}</strong> a <strong>{moneda_destino}</strong>.</div>
"""
        else:
            texto_conversion = f"""
<div class="alert alert-success">Tus <strong>${monto} {moneda_origen}</strong> son <strong>${monto_destino} {moneda_destino}</strong>.</div>
"""

    return render_template("index.html", texto_conversion=texto_conversion, monedas=MONEDAS)

if __name__ == '__main__':
    app.run(debug=True)
