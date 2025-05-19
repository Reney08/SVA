# Routen/zapfstelleRouten.py
from flask import Blueprint, request, jsonify, render_template
from db_helpers import get_db, get_zapf_db

zapfstelle_bp = Blueprint('zapfstelle', __name__, url_prefix='/Zapfstelle')

# -------------------- Seitenrouten --------------------
@zapfstelle_bp.route('/')
def zapfstelle_index():
    return render_template('zapfstelle_index.html')

@zapfstelle_bp.route('/getAll')
def show_all():
    return render_template('zapfstelleGetAll.html')

@zapfstelle_bp.route('/get')
def show_single():
    return render_template('zapfstelleGetSingle.html')

@zapfstelle_bp.route('/delete')
def show_delete():
    return render_template('zapfstelleDelete.html')

@zapfstelle_bp.route('/setZapfstelle')
def show_update():
    return render_template('setZapfstelle.html')

@zapfstelle_bp.route('/add')
def show_add():
    return render_template('zapfstelleAdd.html')

