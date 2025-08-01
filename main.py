import db_connection
import generate_db
from consts import IMDB_TSV_FILE_NAME


def main():
    neo4j_db = db_connection.init_db()
    generate_db.generate_db_from_tsv(IMDB_TSV_FILE_NAME, neo4j_db)


if __name__ == "__main__":
    main()