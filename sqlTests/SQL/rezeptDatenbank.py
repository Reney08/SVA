from datenbankconnector import DatenbankConnector

class RezeptDatenbank:
    def __init__(self, connector: DatenbankConnector):
        self.connector = connector

    def getAllZutaten(self):
        """Returns a list of all ingredients as dicts with id and name."""
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("SELECT ID, Name FROM Zutat")
        result = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        cur.close()
        return result

    def addCocktail(self, Name: str, Beschreibung: str, Zubereitung: str) -> int:
        """Adds a new cocktail and returns its ID (RezeptNR)."""
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute(
            "INSERT INTO Cocktail (Name, Beschreibung, Zubereitung) VALUES (?, ?, ?)",
            (Name, Beschreibung, Zubereitung)
        )
        self.connector.conn.commit()
        rezeptnr = cur.lastrowid
        cur.close()
        return rezeptnr

    def addRezept(self, RezeptNR: int, RezeptPos: int, Zutat: int, Menge: float):
        """Adds a single ingredient to a recipe (Rezept table)."""
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute(
            "INSERT INTO Rezept (RezeptNR, RezeptPos, Zutat, Menge) VALUES (?, ?, ?, ?)",
            (RezeptNR, RezeptPos, Zutat, Menge)
        )
        self.connector.conn.commit()
        cur.close()

    def getAllRezepteWithIngredients(self):
        """Returns all cocktails with their ingredients."""
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("""
            SELECT c.ID, c.Name, c.Beschreibung, c.Zubereitung,
                   r.RezeptPos, r.Menge, z.ID, z.Name
            FROM Cocktail c
            JOIN Rezept r ON c.ID = r.RezeptNR
            JOIN Zutat z ON r.Zutat = z.ID
            ORDER BY c.ID, r.RezeptPos
        """)
        rows = cur.fetchall()
        cur.close()
        # Group results by cocktail
        rezepte = {}
        for row in rows:
            cid = row[0]
            if cid not in rezepte:
                rezepte[cid] = {
                    "ID": cid,
                    "Name": row[1],
                    "Beschreibung": row[2],
                    "Zubereitung": row[3],
                    "Zutaten": []
                }
            rezepte[cid]["Zutaten"].append({
                "RezeptPos": row[4],
                "Menge": row[5],
                "ZutatID": row[6],
                "ZutatName": row[7]
            })
        return list(rezepte.values())

    def getRezeptWithIngredients(self, rezeptnr: int):
        """Returns a single cocktail with its ingredients."""
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("""
            SELECT c.ID, c.Name, c.Beschreibung, c.Zubereitung,
                   r.RezeptPos, r.Menge, z.ID, z.Name
            FROM Cocktail c
            JOIN Rezept r ON c.ID = r.RezeptNR
            JOIN Zutat z ON r.Zutat = z.ID
            WHERE c.ID = ?
            ORDER BY r.RezeptPos
        """, (rezeptnr,))
        rows = cur.fetchall()
        cur.close()
        if not rows:
            return None
        rezept = {
            "ID": rows[0][0],
            "Name": rows[0][1],
            "Beschreibung": rows[0][2],
            "Zubereitung": rows[0][3],
            "Zutaten": []
        }
        for row in rows:
            rezept["Zutaten"].append({
                "RezeptPos": row[4],
                "Menge": row[5],
                "ZutatID": row[6],
                "ZutatName": row[7]
            })
        return rezept

    def deleteRezept(self, rezeptnr: int):
        """Deletes a cocktail and all its recipe entries."""
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        # Delete all Rezept rows for this cocktail
        cur.execute("DELETE FROM Rezept WHERE RezeptNR = ?", (rezeptnr,))
        # Delete the cocktail itself
        cur.execute("DELETE FROM Cocktail WHERE ID = ?", (rezeptnr,))
        self.connector.conn.commit()
        cur.close()
