from typing import Dict, List, Any, Generator

import pandas
import csv

from neo4j_connection import Neo4jConnection


def _add_row_to_db(row, neo4j_db_connection):
    """
    adds a single row to the neo4j database
    the row will always be handled using the names.basic.tsv format of imdb
    #TODO: Support more formats
    :param row: tsv row
    :param neo4j_db_connection:
    :return:
    """
    print(row)

def parse_tsv_to_pandas(imdb_tsv_file_path:str, batch_size:int=200) -> Generator[list[Any], Any, None]:
    """
    parses an imdb name.basics.tsv file and returns a pandas dataframe
    :param batch_size: yields the result after every batch_size rows
    :param imdb_tsv_file_path:
    :return: returns the pandas dataframe
    """
    pandas_dataframe = pandas.read_csv(imdb_tsv_file_path, sep="\t")
    parsed_data = []
    for i, row in pandas_dataframe.iterrows():
        if len(parsed_data) == batch_size:
            print("done parsing row {}".format(i))
            yield parsed_data
            parsed_data = []
        if row['knownForTitles'] == "\\n":
            print("skipping row {} as actor never played any roles".format(i))
            continue
        movies = row['knownForTitles'].split(',') or []
        parsed_data.append({
            "actor_id": row['nconst'],
            "actor_name": row['primaryName'],
            "born_year": row['birthYear'],
            "death_year": row['deathYear'],
            "movies": [{"id": movie.strip()} for movie in movies]
        })
    yield parsed_data

def generate_db_from_tsv(imdb_tsv_file_path: str, neo4j_db_connection:Neo4jConnection):
    """
    converts an imdb tsv file into a parsed neo4j database and loads it into the neo4j database connection
    :param imdb_tsv_file_path: path to the imdb tsv file
    :param neo4j_db_connection: neo4j database connection
    :return:
    """
    for data in parse_tsv_to_pandas(imdb_tsv_file_path):
        neo4j_db_connection.add_pandas_parsed_tsv(data)
    # with open(imdb_tsv_file_path, "r") as imdb_tsv_file:
    #     imdb_tsv_reader = csv.reader(imdb_tsv_file, delimiter="\t")
    #     header = next(imdb_tsv_reader)
    #     for i, row in enumerate(imdb_tsv_reader):
    #         print("{} - Processing actor_id {}".format(i, row[0]))
    #         neo4j_db_connection.parse_and_add_tsv_row_to_db(header, row)
