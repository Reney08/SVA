
# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_cocktail_db

cocktail_bp = Blueprint('zapfstelle', __name__, ) # hier noch den Routenpräfix

# -------------------- API-Routen --------------------
'''
API-Routen sind für die Bereitstellung von Daten im JSON-Format zuständig.
'''
