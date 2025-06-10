from datenbankconnector import DatenbankConnector

class CocktailDatenbank:
    def __init__(self, connector: DatenbankConnector):
        self.connector = connector
        
    #TODO alle python und SQL statements
    '''
    - add route um einen Cocktail hinzuzufügen
    - delete route um einen Cocktail zu löschen
    - set route um einen Cocktail zu verändern
    
    wichtige Hinweise:
    pro Stichpunkt eine Methode
    Methoden haben immer als ersten Parameter self
    prüfe immer am Anfang der Methode ob die Verbindung zur DB besteht
    wenn nicht, dann erstelle die Verbindung
    schließe die Verbindung am Ende der Methode
    '''
        def getAll(self):
            if self.connector.conn in None:
                self.connector.connect()
            cur = self.connector.conn.cursor()
            cur.execute(
                "SELECT * FROM Cocktail"
            )
            result = cur.fetchall()
            cur.close()
            return result

        def getSingle(self, id: int):
            if self.connector.conn is None:
                seld.connector.connect()
            cur = self.connector.conn.cursor()
            cur.execute(
                "SELECT * FROM Cocktail WHERE CocktailID = ? LIMIT 1", (id,)
            )
            result = cur.fetchone
            cur.close()
            return result

        def addCocktail(self, Name: str, Beschreibung: str, ExtLink: str = None) -> int:
            pass

        def deleteCocktail(self):
            pass