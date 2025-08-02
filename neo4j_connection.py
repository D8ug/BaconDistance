from neo4j import GraphDatabase
from consts import DB_URI, DB_USERNAME, DB_PASSWORD_PATH
from db_connection import DBConnection


class Neo4jConnection(DBConnection):
    def __init__(self):
        self.connection = GraphDatabase()
        self.uri = DB_URI
        self.username = DB_USERNAME
        self.password = ''
        with open(DB_PASSWORD_PATH, 'r') as f:
            self.password = f.readline().strip()
        self.connect()

    def connect(self):
        """
        connects to the neo4j database
        :return:
        """
        with open(DB_PASSWORD_PATH, 'r') as f:
            password = f.readline().strip()
        self.connection.driver(DB_URI, auth=(DB_USERNAME, password))

    def close(self):
        """
        close the connection to the neo4j database
        :return:
        """
        self.connection = None #TODO: actually close the connection (tho i dont see a reason to close this connection)