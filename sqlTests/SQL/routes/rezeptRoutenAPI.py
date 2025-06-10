from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_rezept_db

rezept_api_bp = Blueprint('rezeptAPI', __name__, url_prefix='/api/Rezept')

# -------------------- API ROUTES --------------------
@rezept_api_bp.route('/')
def api_index():
    return render_template('rezept_api_index.html')

@rezept_api_bp.route('/zutaten')
def get_zutaten():
    """Return all available ingredients."""
    zutaten = get_rezept_db().getAllZutaten()
    return jsonify(zutaten)

@rezept_api_bp.route('/getAll')
def get_all():
    """Return all cocktails/recipes with their ingredients."""
    rezepte = get_rezept_db().getAllRezepteWithIngredients()
    return jsonify(rezepte)

@rezept_api_bp.route('/get')
def get_single():
    """Return a single recipe with its ingredients."""
    cocktail_id = request.args.get('id', type=int)
    if cocktail_id is None:
        return jsonify({"error": "Missing id parameter"}), 400
    rezept = get_rezept_db().getRezeptWithIngredients(cocktail_id)
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
        cocktail_id = get_rezept_db().addCocktail(
            Name=data['Name'],
            Beschreibung=data['Beschreibung'],
            Zubereitung=data.get('Zubereitung', '')
        )
        for z in data['Zutaten']:
            get_rezept_db().addRezept(
                CocktailID=cocktail_id,
                RezeptPos=z['RezeptPos'],
                ZutatID=z['ZutatID'],
                Menge=z['Menge']
            )
        return jsonify({"status": "added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rezept_api_bp.route('/delete', methods=['DELETE'])
def delete():
    """Delete a recipe (cocktail) and its ingredients."""
    cocktail_id = request.args.get('id', type=int)
    if cocktail_id is None:
        return jsonify({"error": "Missing id parameter"}), 400
    get_rezept_db().deleteRezept(cocktail_id)
    return jsonify({"status": "deleted"})
