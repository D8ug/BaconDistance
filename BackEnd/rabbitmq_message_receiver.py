import json
import os
import sys

import pika

from BackEnd.DB.neo4j_connection import Neo4jConnection

neo4j_db = Neo4jConnection()

def connect_to_rabbit_mq() -> pika.connection:
    """
    connect to rabbitmq server
    :return: pika connection
    """
    return pika.BlockingConnection(pika.ConnectionParameters('localhost'))

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    data = json.loads(body)
    print(f"    [x] Parsed JSON: {data}")
    if "name" not in data or "actors" not in data:
        print("    [x] Invalid json, skipping")
        return
    movie_name = data["name"]
    neo4j_db.add_movie(movie_name)
    for actor in data["actors"]:
        neo4j_db.add_actor_by_name(actor)
        neo4j_db.add_movie_relation(actor, movie_name)

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
    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    connection.close()

if __name__ == '__main__':
    neo4j_db.connect()
    rabbit_mq_manager()


