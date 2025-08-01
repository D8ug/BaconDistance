from neo4j import GraphDatabase
from consts import DB_URI, DB_USERNAME, DB_PASSWORD_PATH


def connect_to_db(neo4j_db_connection:GraphDatabase):
    """
    connects to the neo4j database
    :param neo4j_db_connection: connection to the neo4j database
    :return:
    """
    with open(DB_PASSWORD_PATH, 'r') as f:
        password = f.readline().strip()
    neo4j_db_connection.driver(DB_URI, auth=(DB_USERNAME, password))

def init_db() -> GraphDatabase:
    """
    creates a db objects and connects to the neo4j database
    :return: returns the neo4j database object
    """
    db = GraphDatabase()
    connect_to_db(db)
    return db