# app.py
from flask import Flask, g, render_template

from routes.zapfstelleRouten import zapfstelle_bp
from routes.zapfstelleRoutenAPI import zapfstelle_api_bp
from routes.rezeptRouten import rezept_bp
from routes.rezeptRoutenAPI import rezept_api_bp

app = Flask(__name__)

# Blueprint registrieren
app.register_blueprint(zapfstelle_bp)
app.register_blueprint(zapfstelle_api_bp)

app.register_blueprint(rezept_bp)
app.register_blueprint(rezept_api_bp)
'''
hier die beiden neuen blueprints registrieren
'''
@app.route('/')
def index():
    return render_template('index.html')
# -------------------- Close Database connection --------------------
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        print("Verbindung zur Datenbank geschlossen.")
    else:
        print("Keine Verbindung zur Datenbank vorhanden.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
