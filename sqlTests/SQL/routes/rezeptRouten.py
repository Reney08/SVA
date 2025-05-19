# Routen/coktailRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, ge_rezept_db

rezept_bp = Blueprint('rezept', __name__, url_prefix='/Rezept') # hier den Namen und den Routenpräfix hinzufügen

# -------------------- Seitenrouten --------------------
@rezept_bp.route('/')
def rezept_index():
    return render_template('rezept_index.html')

@rezept_bp.route('/getAll')
def show_all():
    return render_template('rezeptGetAll.html')

@rezept_bp.route('/get')
def show_single():
    return render_template('rezeptGetSingle.html')

@rezept_bp.route('/delete')
def show_delete():
    return render_template('rezeptDelete.html')

@rezept_bp.route('/setRezept')  
def show_update():
    return render_template('setRezept.html')

@rezept_bp.route('/add')
def show_add():
    return render_template('rezeptAdd.html')

