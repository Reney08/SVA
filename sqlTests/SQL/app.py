from flask import Flask, request, jsonify, render_template, g
from datenbankconnector import DatenbankConnector
from zapfstelleDatenbank import ZapfstelleDatenbank

app = Flask(__name__)

# --- Helper functions for per-request DB handling ---

def get_db():
    if 'db' not in g:
        g.db = DatenbankConnector(
            user="vscode",
            password="Keins123!",
            host="db",
            database="BarbotDB",
            port=3306
        )
    return g.db

def get_zapf_db():
    if 'zapf_db' not in g:
        g.zapf_db = ZapfstelleDatenbank(get_db())
    return g.zapf_db

# -------------------- Seitenrouten --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getAll')
def show_all():
    return render_template('getAll.html')

@app.route('/delete')
def show_delete():
    return render_template('delete.html')

@app.route('/setZapfstelle')
def show_update():
    return render_template('setZapfstelle.html')

@app.route('/add')
def show_add():
    return render_template('add.html')  # Optional: add.html if you have it

# -------------------- API-Routen --------------------

@app.route('/api/Zapfstelle/getAll')
def getAll():
    daten = get_zapf_db().getAll()
    return jsonify(daten)

@app.route('/api/Zapfstelle/get')
def getSingle():
    id = request.args.get('id', type=int)
    result = get_zapf_db().getZapfstelle(id)
    return jsonify(result)

@app.route('/api/Zapfstelle/add', methods=['POST'])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400
    try:
        get_zapf_db().addZapfstelle(
            SchienenPos=data['SchienenPos'],
            Pumpe=data['Pumpe'],
            PumpenNR=data['PumpenNR'],
            Fuellmenge=data['Fuellmenge']
        )
        return jsonify({"status": "added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/Zapfstelle/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id', type=int)
    get_zapf_db().deleteZapfstelle(id)
    return jsonify({"status": "deleted"})

@app.route('/api/Zapfstelle/set', methods=['POST'])
def setZapfstelle():
    data = request.get_json()
    id = data.get("id")
    try:
        zapf_db = get_zapf_db()
        if data.get("schienenPos") is not None:
            zapf_db.updateSchienenPos(id, int(data["schienenPos"]))
        if data.get("pumpe") in ["true", "false"]:
            zapf_db.updatePumpe(id, data["pumpe"] == "true")
        if data.get("pumpenNr") is not None:
            zapf_db.updatePumpenNr(id, int(data["pumpenNr"]))
        if data.get("fuellmenge") is not None:
            zapf_db.updateFuellmenge(id, int(data["fuellmenge"]))
        return jsonify({"status": "updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- Close Database connection --------------------

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        print("Verbindung zur Datenbank geschlossen.")
    else:
        print("Keine Verbindung zur Datenbank vorhanden.")

# -------------------- Start Server --------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
