from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['GET'])
def hello():
    return jsonify({"message": "test info"})

@app.route('/api/get_bacon_distance', methods=['POST'])
def calc_bacon_distance():
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
