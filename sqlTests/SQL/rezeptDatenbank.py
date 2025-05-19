from datenbankconnector import DatenbankConnector

class RezeptDatenbank:
    def __init__(self, connector: DatenbankConnector):
        self.connector = connector

    def getAll(self):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("SELECT * FROM Rezept")
        result = cur.fetchall()
        cur.close()
        return result
    
    def getRezept(self, id: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("SELECT * FROM Rezept WHERE RezeptID = ? LIMIT 1", (id,))
        result = cur.fetchone()
        cur.close()
        return result
    
    def addRezept(self, Name: str, Beschreibung: str, Zutaten: str, Zubereitung: str):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("INSERT INTO Rezept (Name, Beschreibung, Zutaten, Zubereitung) VALUES (?, ?, ?, ?)", (Name, Beschreibung, Zutaten, Zubereitung))
        self.connector.conn.commit()
        cur.close()
        
    def deleteRezept(self, id: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("DELETE FROM Rezept WHERE RezeptID = ?", (id,))
        self.connector.conn.commit()
        cur.close()