from consts import Neo4jQuery
from neo4j_connection import Neo4jConnection


def bacon_distance(neo4j_db_connection: Neo4jConnection, actor_name:str) -> float:
    """
    returns the bacon distance of a given actor
    NOTE: This will always calculate the distance to Kevin Bacon!
    :param neo4j_db_connection: the neo4j db connection
    :param actor_name: the target actor name
    :return: returns the bacon distance and INF if there's no bacon distance
    """
    result = neo4j_db_connection.session.run(Neo4jQuery.CALCULATE_BACON_DISTANCE_FORMAT.value.format(target=actor_name))
    result = result.single()
    return result["hops"]