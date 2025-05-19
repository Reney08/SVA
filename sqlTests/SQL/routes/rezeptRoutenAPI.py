from flask import Blueprint, request, jsonify
from db_helpers import ge_rezept_db

rezept_api_bp = Blueprint('rezeptAPI', __name__, url_prefix='/api/Rezept')

# -------------------- API ROUTES --------------------
@rezept_api_bp.route('/')
def api_index():
    return render_template('rezept_api_index.html')

@rezept_api_bp.route('/zutaten')
def get_zutaten():
    """Return all available ingredients."""
    zutaten = ge_rezept_db().getAllZutaten()
    return jsonify(zutaten)

@rezept_api_bp.route('/getAll')
def get_all():
    """Return all cocktails/recipes with their ingredients."""
    rezepte = ge_rezept_db().getAllRezepteWithIngredients()
    return jsonify(rezepte)

@rezept_api_bp.route('/get')
def get_single():
    """Return a single recipe with its ingredients."""
    rezeptnr = request.args.get('id', type=int)
    if rezeptnr is None:
        return jsonify({"error": "Missing id parameter"}), 400
    rezept = ge_rezept_db().getRezeptWithIngredients(rezeptnr)
    if rezept is None:
        return jsonify({"error": "Rezept not found"}), 404
    return jsonify(rezept)

@rezept_api_bp.route('/add', methods=['POST'])
def add():
    """Add a new recipe (cocktail) and its ingredients."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400
    try:
        rezeptnr = ge_rezept_db().addCocktail(
            Name=data['Name'],
            Beschreibung=data['Beschreibung'],
            Zubereitung=data['Zubereitung']
        )
        for z in data['Zutaten']:
            ge_rezept_db().addRezept(
                RezeptNR=rezeptnr,
                RezeptPos=z['RezeptPos'],
                Zutat=z['Zutat'],
                Menge=z['Menge']
            )
        return jsonify({"status": "added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rezept_api_bp.route('/delete', methods=['DELETE'])
def delete():
    """Delete a recipe (cocktail) and its ingredients."""
    rezeptnr = request.args.get('id', type=int)
    if rezeptnr is None:
        return jsonify({"error": "Missing id parameter"}), 400
    ge_rezept_db().deleteRezept(rezeptnr)
    return jsonify({"status": "deleted"})
