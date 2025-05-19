# Routen/zapfstelleRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_zapf_db

zapfstelle_api_bp = Blueprint('zapfstelleAPI', __name__, url_prefix='/api/Zapfstelle')

# -------------------- API-Routen --------------------
@zapfstelle_api_bp.route('/getAll')
def getAll():
    daten = get_zapf_db().getAll()
    return jsonify(daten)

@zapfstelle_api_bp.route('/api/Zapfstelle/get')
def getSingle():
    id = request.args.get('id', type=int)
    result = get_zapf_db().getZapfstelle(id)
    return jsonify(result)

@zapfstelle_api_bp.route('/api/Zapfstelle/add', methods=['POST'])
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

@zapfstelle_api_bp.route('/api/Zapfstelle/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id', type=int)
    get_zapf_db().deleteZapfstelle(id)
    return jsonify({"status": "deleted"})

@zapfstelle_api_bp.route('/api/Zapfstelle/set', methods=['POST'])
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
