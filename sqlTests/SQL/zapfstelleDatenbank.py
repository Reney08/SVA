from datenbankconnector import DatenbankConnector

class ZapfstelleDatenbank:
    def __init__(self, connector: DatenbankConnector):
        self.connector = connector

    def getAll(self):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("SELECT * FROM Zapfstelle")
        result = cur.fetchall()
        cur.close()
        return result
    
    #TODO id kommt von Usereingabe
    def getZapfstelle(self, id: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("SELECT * FROM Zapfstelle WHERE ZapfstelleID = ? LIMIT 1", (id,))
        result = cur.fetchone()
        cur.close()
        return result
    
    #TODO Usereingabe im Switch case
    def setZapfstelle(self, input: int):
        match input:
            case "1":
                self.updateSchienenPos(1, 50)
            case "2":
                self.updatePumpe(1, False)
            case "3":
                self.updatePumpenNr(1, 10)
            case "14":
                self.updateFuellmenge(1, 100)
    
    #TODO Usereingebe für werte
    def addZapfstelle(self, SchienenPos: int, Pumpe: bool, PumpenNR: int, Fuellmenge: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("INSERT INTO Zapfstelle (SchienenPos, Pumpe, PumpenNR, Fuellmenge) VALUES (?, ?, ?, ?)", (SchienenPos, Pumpe, PumpenNR, Fuellmenge))
        self.connector.conn.commit()
        cur.close()
        
    #TODO id kommt von Usereingabe
    def deleteZapfstelle(self, id: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("DELETE FROM Zapfstelle WHERE ZapfstelleID = ?", (id,))
        self.connector.conn.commit()
        cur.close()
        
    def updateSchienenPos(self, id: int, SchienenPos: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("UPDATE Zapfstelle SET SchienenPos = ? WHERE ZapfstelleID = ?", (SchienenPos, id))
        self.connector.conn.commit()
        cur.close()
        
    def updatePumpe(self, id: int, Pumpe: bool):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("UPDATE Zapfstelle SET Pumpe = ? WHERE ZapfstelleID = ?", (Pumpe, id))
        self.connector.conn.commit()
        cur.close()
        
    def updatePumpenNr(self, id: int, PumpenNR: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("UPDATE Zapfstelle SET PumpenNR = ? WHERE ZapfstelleID = ?", (PumpenNR, id))
        self.connector.conn.commit()
        cur.close()
        
    def updateFuellmenge(self, id: int, Fuellmenge: int):
        if self.connector.conn is None:
            self.connector.connect()
        cur = self.connector.conn.cursor()
        cur.execute("UPDATE Zapfstelle SET Fuellmenge = ? WHERE ZapfstelleID = ?", (Fuellmenge, id))
        self.connector.conn.commit()
        cur.close()

if __name__ == "__main__":
    connector = DatenbankConnector(
        user="barbot",
        password="Keins123!",
        host="10.22.41.18",
        database="BarbotDB",
        port=3306
    )
    
    connector.connect()
    zapf_db = ZapfstelleDatenbank(connector)
    # daten = zapf_db.addZapfstelle(1, True, 2, 100)1
    userinput = input("Was möchten Sie tun?\n1. SchienenPos ändern\n2. Pumpenstatus ändern\n3. PumpenNummer ändern\n4. Fuellmengen ändern\n")
    zapf_db.setZapfstelle(userinput)
    daten = zapf_db.getAll()
    for row in daten:
        print(row)
    connector.close()
