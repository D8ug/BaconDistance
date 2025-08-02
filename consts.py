from enum import Enum


DB_URI = "neo4j://127.0.0.1:7687"
DB_USERNAME = "neo4j"
DB_PASSWORD_PATH = "C:\password.txt" #TODO: Find a better way to do this, for now i dont want this to be in the repo
IMDB_TSV_FILE_NAME = "name.basic.tsv"

class Neo4jQuery(Enum):
    ADD_ACTOR_FORMAT = """
        MERGE (a:Actor {{id: {actor_id}}})
        SET a.name = {actor_name}
        SET a.born_year = {born_year}
        SET a.death_year = {death_year}
    """
    ADD_MOVIE_FORMAT = """
        MERGE (a:Movie {{id: {movie_id}}})
    """
    ADD_ACTOR_ROLE_FORMAT = """
    MATCH(a:Actor {{id: {actor_id}}}), (m:Movie {{id: {movie_id}}})
    MERGE (a)-[:ACTED_IN]->(m)
    """
