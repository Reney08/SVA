# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_cocktail_db

cocktail_bp = Blueprint('placeholder', __name__, url_prefix='/Cocktail') # hier den Namen und den Routenpräfix hinzufügen

# -------------------- Seitenrouten --------------------
'''
Seitenrouten sind für die Darstellung von HTML-Seiten zuständig.
'''

