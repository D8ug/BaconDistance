from flask import Flask, jsonify, request
from flask_cors import CORS

from DB import bacon_distance
from DB.neo4j_connection import Neo4jConnection


neo4j_connection = Neo4jConnection()

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def hello():
    return jsonify({"message": "test info"})

@app.route('/api/get_bacon_distance', methods=['GET'])
def calc_bacon_distance():
    actor = request.args.get('actor')  # should be in a format of ?actor=Tom%20Hanks
    return jsonify({"result": bacon_distance.bacon_distance(neo4j_connection, actor)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
