# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_cocktail_db

cocktail_bp = Blueprint('cocktail', __name__, url_prefix='/Cocktail') # hier den Namen und den Routenpräfix hinzufügen

# -------------------- Seitenrouten --------------------
@cocktail_bp.route('/')
def cocktail_index():
    return render_template("cocktail_index.html")

@cocktail_bp.route('/getAll')
def getAll():
    return render_template('cocktailGetAll.html')

@cocktail_bp.route('/get')
def getSingle():
    return render_template('cocktailGetSingle.html')
