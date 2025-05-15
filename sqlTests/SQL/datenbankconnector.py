import mariadb
import sys

class DatenbankConnector:
    def __init__(self, user, password, host, database, port):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            print("Verbindung zur Datenbank aufgebaut.")
        except mariadb.Error as e:
            print(f"Fehler beim Verbinden: {e}")
            sys.exit(1)

    def close(self):
        if self.conn:
            self.conn.close()
            print("Verbindung zur Datenbank geschlossen.")
