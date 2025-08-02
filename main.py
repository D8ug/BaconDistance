import db_connection
import generate_db
from consts import IMDB_TSV_FILE_NAME
from neo4j_connection import Neo4jConnection


def main():
    neo4j_db = Neo4jConnection()
    generate_db.generate_db_from_tsv(IMDB_TSV_FILE_NAME, neo4j_db)


if __name__ == "__main__":
    main()