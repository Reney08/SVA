
# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_cocktail_db

cocktail_bp = Blueprint('placeholder', __name__, url_prefix='/api/Cocktail') # hier den Namen und den Routenpräfix hinzufügen

# -------------------- API-Routen --------------------
'''
API-Routen sind für die Bereitstellung von Daten im JSON-Format zuständig.
'''
