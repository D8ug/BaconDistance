from neo4j import GraphDatabase
import csv

from neo4j_connection import Neo4jConnection


def _add_row_to_db(row, neo4j_db_connection):
    """
    adds a single row to the neo4j database
    the row will always be handled using the names.basic.tsv format of imdb
    #TODO: Support more formats
    :param row: tsv row
    :param neo4j_db_connection:
    :return:
    """
    print(row)

def generate_db_from_tsv(imdb_tsv_file_path: str, neo4j_db_connection:Neo4jConnection):
    """
    converts an imdb tsv file into a parsed neo4j database and loads it into the neo4j database connection
    :param imdb_tsv_file_path: path to the imdb tsv file
    :param neo4j_db_connection: neo4j database connection
    :return:
    """

    with open(imdb_tsv_file_path, "r") as imdb_tsv_file:
        imdb_tsv_reader = csv.reader(imdb_tsv_file, delimiter="\t")
        header = next(imdb_tsv_reader)
        for row in imdb_tsv_reader:
            neo4j_db_connection.parse_and_add_tsv_row_to_db(header, row)
