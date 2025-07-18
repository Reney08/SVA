# db_helpers.py
from flask import g
from datenbankconnector import DatenbankConnector
from zapfstelleDatenbank import ZapfstelleDatenbank
from cocktailDatenbank import CocktailDatenbank
from rezeptDatenbank import RezeptDatenbank

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

def get_cocktail_db():
    if 'cocktail_db' not in g:
        g.cocktail_db = CocktailDatenbank(get_db())
    return g.cocktail_db

def get_rezept_db():
    if 'rezept_db' not in g:
        g.rezept_db = RezeptDatenbank(get_db())
    return g.rezept_db
