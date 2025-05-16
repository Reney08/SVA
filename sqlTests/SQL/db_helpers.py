# db_helpers.py
from flask import g
from datenbankconnector import DatenbankConnector
from zapfstelleDatenbank import ZapfstelleDatenbank

def get_db():
    if 'db' not in g:
        g.db = DatenbankConnector(
            user="vscode",
            password="Keins123!",
            host="db",
            database="BarbotDB",
            port=3306
        )
    return g.db

def get_zapf_db():
    if 'zapf_db' not in g:
        g.zapf_db = ZapfstelleDatenbank(get_db())
    return g.zapf_db
