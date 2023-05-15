from flask import Flask, request, render_template
import datetime
import requests
TASA_CLP_FILE = "tasa_clp.txt"
TASA_CLP = None

def save_tasa_clp(tasa_clp, date):
    with open(TASA_CLP_FILE, "a") as file:
        file.write(f"{tasa_clp},{date}\n")

def load_tasa_clp(date):
    with open(TASA_CLP_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")
            file_date = datetime.datetime.strptime(data[1], "%Y-%m-%d").date()
            if file_date == date:
                tasa_clp = float(data[0])
                return tasa_clp, file_date
    raise FileNotFoundError

def fetch_dolar_by_day(year, month, day, acarreadas=None):
    global TASA_CLP
    if acarreadas is None:
        acarreadas = []

    if TASA_CLP is not None:
        return TASA_CLP

    try:
        date = datetime.date(year, month, day)
        TASA_CLP, file_date = load_tasa_clp(date)
        return TASA_CLP
    except FileNotFoundError:
        pass

    r = requests.get("https://mindicador.cl/api/dolar/{day}-{month}-{year}".format(day=day, month=month, year=year))
    if r.status_code == 200:
        try:
            data = r.json()
            TASA_CLP = data["serie"][0]["valor"]
            for fecha_ac in acarreadas:
                save_tasa_clp(TASA_CLP, fecha_ac)
            save_tasa_clp(TASA_CLP, date)
            return TASA_CLP
        except IndexError:
            # Restar un día a la fecha y volver a intentar
            previous_day = datetime.date(year, month, day) - datetime.timedelta(days=1)
            acarreadas.append(date)
            return fetch_dolar_by_day(previous_day.year, previous_day.month, previous_day.day, acarreadas=acarreadas)
          
        except Exception:
            raise ValueError(f"La API mindicador.cl no retorno un valor conocido. Revisar: '{data}'")

now = datetime.datetime.now() # fecha de hoy para calculo de tasas
TASAS = {
    "CLP": fetch_dolar_by_day(now.year, now.month, now.day),
    "AR": 173.66,
    "MX": 19.76,
    "CO": 4782.22,
    "USD": 1,
    "PE": 3.72
}

MONEDAS = list(TASAS.keys()) # ["chilenos", "argentinos", ...]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    texto_conversion = None
    monto = None
    moneda_origen = None
    moneda_destino = None
    if request.method == 'POST':
        monto = request.form['monto']
        if not monto.isdigit():
            texto_conversion = f"""
                <div class="alert alert-danger">TIENES QUE PONER UN MONTO CORRECTO, ZOQUETE</div>
            """
        else:
            moneda_origen = request.form['moneda_origen']
            tc_dolar = TASAS[moneda_origen]
            dolares = int(monto) / tc_dolar
            moneda_destino = request.form['moneda_destino']
            if moneda_origen == moneda_destino:
                texto_conversion = f"""
                    <div class="alert alert-danger">¿Por qué quieres convertir <strong>${moneda_origen}</strong> a <strong>${moneda_destino}</strong>? ZOQUETE</div>
                """
            else:
                tc_pesos = TASAS[moneda_destino]
                monto_destino = round(dolares * tc_pesos, 2)
                texto_conversion = f"""
                    <div class="alert alert-success">Tus <strong>${monto} {moneda_origen}</strong> son <strong>${monto_destino} {moneda_destino}</strong>.</div>
                """ 

    return render_template("index.html", texto_conversion=texto_conversion, monedas=MONEDAS, monto=monto, moneda_origen=moneda_origen, moneda_destino = moneda_destino, request=request)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
