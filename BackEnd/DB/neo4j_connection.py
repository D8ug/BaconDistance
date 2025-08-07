import os
from typing import List

from neo4j import GraphDatabase
from neo4j.exceptions import ClientError

from DB.consts import Neo4jQuery
from DB.db_connection import DBConnection


class Neo4jConnection(DBConnection):
    def __init__(self):
        self.connection = GraphDatabase()
        self.uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        self.username = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "")
        self.driver = None
        self.session = None
        self.connect()
        self.init_graph()

    def connect(self):
        """
        connects to the neo4j database
        :return:
        """
        self.driver = self.connection.driver(self.uri, auth=(self.username, self.password))
        self.session = self.driver.session()
        try:
            self.session.run("RETURN 1")
            print("Connected to neo4j successfully")
        except:
            assert("Connection to Neo4j DB failed")

    def refresh_graph(self):
        """
        For running the spf algorithm on the neo4j database we need to init a movie/actor graph on the db
        This function queries the db to do so, so the algorithm will then work.
        for some reason, using the same graph each time breaks so i will delete it before starting it
        :return:
        """
        self.session.run(Neo4jQuery.DELETE_GRAPH_QUERY.value)
        try:
            self.session.run(Neo4jQuery.INIT_GRAPH_QUERY.value)
        except ClientError:
            print("Graph already exists")

    def init_graph(self):
        """
        You must have actor and movie nodes and a relation of acted_in for everything to work so we are
        creating a "fake" actor and movie and relation between them.
        This is really bad practice but I am yet to find a better way to do this
        # TODO: find a better way to do this
        :return:
        """
        self.session.run(Neo4jQuery.INIT_ACTOR_NODES_QUERY.value)
        self.session.run(Neo4jQuery.INIT_MOVIE_NODES_QUERY.value)
        self.session.run(Neo4jQuery.CREATE_EMPTY_RELATION_QUERY.value)
        self.refresh_graph()


    def add_movie(self, movie):
        """
        adds a movie id to the neo4j database if doesn't exist already
        :param movie: the movie id
        :return:
        """
        self.session.run(Neo4jQuery.ADD_MOVIE_FORMAT.value.format(movie_id=movie))

    def add_movie_relation(self, actor_name: str, movie_id: str):
        """
        adds an actor-played_in->movie relation to the db
        :param actor_name:
        :param movie_id:
        :return:
        """
        self.session.run(Neo4jQuery.ADD_ACTOR_ROLE_FORMAT.value.format(actor_name=actor_name, movie_id=movie_id))

    def add_actor_by_name(self, actor_name):
        """
        create an actor node with limited info only based on name
        is used for the rabbitmq db queue as no id is provided
        - checks if the name exists, if so does nothing
        - else creates the actor with an id that is equal to the name of the actor
        :param actor_name:
        :return:
        """
        self.session.run(Neo4jQuery.ADD_ACTOR_BY_NAME_FORMAT.value.format(actor_name=actor_name))

    def add_actor(self, actor_id: str, actor_name: str, born_year: int, death_year: int):
        """
        adds an actor to the neo4j database
        :param actor_id: the actor id from the tsv file
        :param actor_name: the actor's name
        :param born_year: the actor's born year
        :param death_year: the actor's death year
        :return:
        """
        self.session.run(Neo4jQuery.ADD_ACTOR_FORMAT.value.format(actor_id=actor_id,
                                                 actor_name=actor_name,
                                                 born_year=born_year,
                                                 death_year=death_year))

    def _add_tsv_actor_row(self, actor_id: str, actor_name: str, born_year: int, death_year: int, role_ids: List[str]):
        """
        adds a relation to the neo4j database for an actor
        formatted as a (:Actor)-[:ACTED_IN]->(:Movie) relation
        :param actor_id:
        :param actor_name:
        :param role_ids:
        :return:
        """
        self.add_actor(actor_id, actor_name, born_year, death_year)
        for movie in role_ids:
            self.add_movie(movie)
            self.add_movie_relation(actor_name, movie)

    def close(self):
        """
        close the connection to the neo4j database
        :return:
        """
        self.connection = None  # TODO: actually close the connection (tho i dont see a reason to close this connection)

    def add_pandas_parsed_tsv(self, pandas_data):
        self.session.run(Neo4jQuery.ADD_TSV_AS_BATCH_QUERY.value, data=pandas_data)

    def parse_and_add_tsv_row_to_db(self, header, row):
        """
        parses the tsv row and adds it to the neo4j database
        # TODO: parse based on the header! right now we are using magics for optimisition
        :param header: the tsv header (is not currently used)
        :param row: the tsv row that will be added to the neo4j database
        :return:
        """
        if (row[-1] == "\\N"):
            print("skipping {actor_id} as they've never played any role".format(actor_id=row[0]))
            return
        self._add_tsv_actor_row(actor_id=row[0],
                                actor_name=row[1],
                                born_year=row[2],
                                death_year=row[3],
                                role_ids=row[-1].split(","))