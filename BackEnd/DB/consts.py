from enum import Enum


DEFAULT_DB_URI = "bolt://neo4j:7687"
DEFAULT_DB_USERNAME = "neo4j"
IMDB_TSV_FILE_NAME = r"./DB/name.basics.tsv"

class Neo4jQuery(Enum):
    DELETE_GRAPH_QUERY = "CALL gds.graph.drop('actorMovieGraph', false)"
    INIT_ACTOR_NODES_QUERY = "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Actor) REQUIRE a.id IS UNIQUE"
    INIT_MOVIE_NODES_QUERY = "CREATE CONSTRAINT IF NOT EXISTS FOR (m:Movie) REQUIRE m.id IS UNIQUE"
    CREATE_EMPTY_RELATION_QUERY = """
MERGE (a:Actor {id: 'test_actor'})
MERGE (m:Movie {id: 'test_movie'})
MERGE (a)-[:ACTED_IN]->(m)"""
    INIT_GRAPH_QUERY = """
CALL gds.graph.project(
'actorMovieGraph',
['Actor', 'Movie'],
{
ACTED_IN: {
  type: 'ACTED_IN',
  orientation: 'UNDIRECTED'
}
}
);
"""
    ADD_ACTOR_FORMAT = """
MERGE (a:Actor {{id: "{actor_id}"}})
SET a.name = "{actor_name}"
SET a.born_year = "{born_year}"
SET a.death_year = "{death_year}"
    """
    ADD_ACTOR_BY_NAME_FORMAT = """
OPTIONAL MATCH (a:Actor {{name: "{actor_name}"}})
WITH a
WHERE a IS NULL
CREATE (c:Actor {{name: "{actor_name}", id: "{actor_name}"}})
"""
    ADD_MOVIE_FORMAT = """
MERGE (a:Movie {{id: "{movie_id}"}})
    """
    ADD_ACTOR_ROLE_FORMAT = """
MATCH(a:Actor {{name: "{actor_name}"}}), (m:Movie {{id: "{movie_id}"}})
MERGE (a)-[:ACTED_IN]->(m)
    """
    ADD_TSV_AS_BATCH_QUERY = """
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
