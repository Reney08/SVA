from datenbankconnector import DatenbankConnector

class CocktailDatenbank:
    def __init__(self, connector: DatenbankConnector):
        self.connector = connector
        
    #TODO alle python und SQL statements
    '''
    - getAll route um alle Cocktails zu bekommen
    - getSingle route um einen Cocktail zu bekommen
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
