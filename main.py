from DB import bacon_distance, generate_db
from DB.consts import IMDB_TSV_FILE_NAME
from DB.neo4j_connection import Neo4jConnection


def milestone_0(neo4j_db):
    generate_db.generate_db_from_tsv(IMDB_TSV_FILE_NAME, neo4j_db)

def milestone_1(neo4j_db):
    bd = bacon_distance.bacon_distance(neo4j_db, "Tom Hanks")
    print(bd)


def main():
    neo4j_db = Neo4jConnection()
    milestone_0(neo4j_db)
    milestone_1(neo4j_db)


if __name__ == "__main__":
    main()