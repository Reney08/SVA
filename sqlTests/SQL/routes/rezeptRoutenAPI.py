
# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, ge_rezept_db

rezept_api_bp = Blueprint('rezeptAPI', __name__, url_prefix='/api/Rezept') # hier den Namen und den Routenpräfix hinzufügen

# -------------------- API-Routen --------------------
@rezept_api_bp.route('/getAll')
def getAll():
    daten = ge_rezept_db().getAll()
    return jsonify(daten)

@rezept_api_bp.route('/api/Rezept/get')
def getSingle():
    id = request.args.get('id', type=int)
    result = ge_rezept_db().getRezept(id)
    return jsonify(result)

@rezept_api_bp.route('/api/Rezept/add', methods=['POST'])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400
    try:
        ge_rezept_db().addRezept(
            Name=data['Name'],
            Beschreibung=data['Beschreibung'],
            Zutaten=data['Zutaten'],
            Zubereitung=data['Zubereitung']
        )
        return jsonify({"status": "added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@rezept_api_bp.route('/api/Rezept/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id', type=int)
    ge_rezept_db().deleteRezept(id)
    return jsonify({"status": "deleted"})