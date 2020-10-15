from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.json['name']
        return jsonify({'name': name})

    if request.method == 'GET':
        return jsonify({'intro': 'hi'})
