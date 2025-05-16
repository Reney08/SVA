# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_cocktail_db

cocktail_bp = Blueprint('zapfstelle', __name__, ) # hier noch den Routenpräfix

# -------------------- Seitenrouten --------------------
'''
Seitenrouten sind für die Darstellung von HTML-Seiten zuständig.
'''

