
# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_cocktail_db

cocktail_bp = Blueprint('cocktailAPI', __name__, url_prefix='/api/Cocktail') # hier den Namen und den Routenpräfix hinzufügen

# -------------------- API-Routen --------------------
@cocktail_api_bp.route('/')
def api_index():
    return render_template('cocktail_api_index.html')

@cocktail_api_bp('/getAll')
def get_all():
    """Return all cocktails"""
    cocktails = get_cocktail_db().getAll()
    return jsonify(cocktails)

@cocktail_api_bp('/get')
def get_single():
    """Return a single cocktail"""
    cocktail_id = request.args.get('id', type=int)
    if cocktail_id is None
        return jsonify({"error": "Missing id parameter"}), 400
    cocktail = get_cocktail_db().getSingle(cocktail_id)
    if cocktail is None:
        return jsonify({"error": "Cocktail not found"}), 400
    return jsonify(cocktail)

