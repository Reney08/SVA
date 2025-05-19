def getAllRezepteWithIngredients(self):
    if self.connector.conn is None:
        self.connector.connect()
    cur = self.connector.conn.cursor()
    cur.execute("""
        SELECT c.CocktailID, c.Name, c.Beschreibung, c.ExtLink,
               r.RezeptPos, r.Menge, z.ZutatID, z.Name
        FROM Cocktail c
        JOIN Rezept r ON c.CocktailID = r.CocktailID
        JOIN Zutat z ON r.ZutatID = z.ZutatID
        ORDER BY c.CocktailID, r.RezeptPos
    """)
    rows = cur.fetchall()
    cur.close()
    rezepte = {}
    for row in rows:
        cid = row[0]
        if cid not in rezepte:
            rezepte[cid] = {
                "CocktailID": cid,
                "Name": row[1],
                "Beschreibung": row[2],
                "ExtLink": row[3],
                "Zutaten": []
            }
        rezepte[cid]["Zutaten"].append({
            "RezeptPos": row[4],
            "Menge": row[5],
            "ZutatID": row[6],
            "ZutatName": row[7]
        })
    return list(rezepte.values())
