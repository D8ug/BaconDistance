from enum import Enum


DB_URI = "neo4j://127.0.0.1:7687"
DB_USERNAME = "neo4j"
DB_PASSWORD_PATH = r"C:\password.txt" #TODO: Find a better way to do this, for now i dont want this to be in the repo
IMDB_TSV_FILE_NAME = r"name.basics.tsv"

class Neo4jQuery(Enum):
    ADD_ACTOR_FORMAT = """
MERGE (a:Actor {{id: "{actor_id}"}})
SET a.name = "{actor_name}"
SET a.born_year = "{born_year}"
SET a.death_year = "{death_year}"
    """
    ADD_MOVIE_FORMAT = """
MERGE (a:Movie {{id: "{movie_id}"}})
    """
    ADD_ACTOR_ROLE_FORMAT = """
MATCH(a:Actor {{id: "{actor_id}"}}), (m:Movie {{id: "{movie_id}"}})
MERGE (a)-[:ACTED_IN]->(m)
    """
    ADD_TSV_AS_BUTCH_QUERY = """
UNWIND $data AS row
MERGE (a:Actor {id: row.actor_id})
SET a.name = row.actor_name,
    a.born_year = row.born_year,
    a.death_year = row.death_year
WITH a, row

UNWIND row.movies AS movie
MERGE (m:Movie {id: movie.id})
MERGE (a)-[:ACTED_IN]->(m)
    """
    CALCULATE_BACON_DISTANCE_FORMAT = """
MATCH (start:Actor {{name: 'Kevin Bacon'}}), (end:Actor {{name: '{target}'}})
CALL gds.shortestPath.dijkstra.stream(
'actorMovieGraph',
{{
sourceNode: start,
targetNode: end
}}
)
YIELD path, totalCost
RETURN
[node IN nodes(path) WHERE 'Actor' IN labels(node) | node.name] AS Path,
totalCost / 2 AS hops"""
