# app.py
from flask import Flask, g
from routes.zapfstelleRouten import zapfstelle_bp

app = Flask(__name__)

# Blueprint registrieren
app.register_blueprint(zapfstelle_bp)

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
