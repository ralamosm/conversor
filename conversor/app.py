from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    texto_conversion = ''
    if request.method == 'POST':
        monto = request.form['monto']
        moneda_origen = request.form['moneda_origen']
        moneda_destino = request.form['moneda_destino']
        monto_destino = None

        if moneda_destino == 'us' and moneda_origen == 'cl':
            monto_destino = int(monto) / 800.0
        elif moneda_destino == 'cl' and moneda_origen == 'us':
            monto_destino = int(monto) * 800.0

        if monto_destino is None:
            texto_conversion = f"""
<p>Quieres convertir <strong>${monto} {moneda_origen}</strong> a <strong>{moneda_destino}</strong>.</p>
"""
        else:
            texto_conversion = f"<p>Tus <strong>${monto} {moneda_origen}</strong> son <strong>${monto_destino} {moneda_destino}</strong>.</p>"

    return f"""
<h1>Conversor de monedas</h1>
<!-- aca va text_conversion, entramos por {request.method} -->
{texto_conversion}
<!-- aca termina texto_conversion -->
<form method="POST">
    <label for="monto">
        Cuanto tienes para convertir?
        <input type="text" name="monto" value="0" />
    </label>

    <label for="moneda_origen">
        Que moneda es?
        <select name="moneda_origen">
            <option value="cl">CLP</option>
            <option value="ar">ARG</option>
            <option value="co">COL</option>
            <option value="mx">MEX</option>
            <option value="us">USD</option>
        </select>
    </label>

    <label for="moneda_destino">
        A que moneda quieres convertir?
        <select name="moneda_destino">
            <option value="cl">CLP</option>
            <option value="ar">ARG</option>
            <option value="co">COL</option>
            <option value="mx">MEX</option>
            <option value="us">USD</option>
        </select>
    </label>

    <input type="submit" name="submit" value="Convertir" />
</form>
"""

if __name__ == '__main__':
    app.run(debug=True)
