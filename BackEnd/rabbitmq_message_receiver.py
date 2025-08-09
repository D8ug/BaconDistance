import json
import os
import sys
import logging

import pika

from DB.neo4j_connection import Neo4jConnection

neo4j_db = Neo4jConnection()

def connect_to_rabbit_mq() -> pika.connection:
    """
    connect to rabbitmq server
    :return: pika connection
    """
    return pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

def callback(ch, method, properties, body):
    logging.debug(f" [x] Received {body}")
    data = json.loads(body)
    logging.debug(f"    [x] Parsed JSON: {data}")
    if "name" not in data or "actors" not in data:
        logging.debug("    [x] Invalid json, skipping")
        return
    movie_name = data["name"]
    neo4j_db.add_movie(movie_name)
    for actor in data["actors"]:
        neo4j_db.add_actor_by_name(actor)
        neo4j_db.add_movie_relation(actor, movie_name)
    # TODO: this can cause a race where when the graph is deleted and then getting refreshed with the new data
    # Someone might query a request at the same time the graph is starting and it will raise an error
    # I need to fix this by "retrying" a few times in the backend when getting an error that the graph is not
    # initialized
    neo4j_db.refresh_graph()

def rabbit_mq_manager():
    """
    manages the rabbitmq connection
    :return:
    """
    connection = connect_to_rabbit_mq()
    channel = connection.channel()
    channel.queue_declare(queue='newMoviesQueue', durable=True)
    channel.basic_consume(queue='newMoviesQueue',
                          auto_ack=True,
                          on_message_callback=callback)
    logging.debug(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.error('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    connection.close()

if __name__ == '__main__':
    logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout
    )
    logging.debug("Starting rabbitmq message receiver")
    logging.debug("Connecting to the database")
    neo4j_db.connect()
    logging.debug("Connected to the database")
    logging.debug("Starting rabbitmq message receiver manager")
    rabbit_mq_manager()


