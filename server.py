from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash
import os
import uuid
import json

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'


@app.route('/hello', methods=['POST'])
def hey():
    jsonFile = open('data.json', 'r')
    stats = json.load(jsonFile)
    jsonFile.close()
    data = request.get_json()
    uniqueID = data['uniqueID']
    if not uniqueID:
        uniqueID = str(uuid.uuid4())
        stats.append({'uniqueID': uniqueID, 'numberOfVisits': 1})
        jsonFile = open('data.json', 'w')
        jsonFile.write(json.dumps(stats, ensure_ascii=True))
        jsonFile.close()
        return jsonify({"uniqueID": uniqueID})
    else:
        for stat in stats:
            if stat['uniqueID'] == uniqueID:
                try:
                    stat['numberOfVisits'] = int(stat['numberOfVisits']) + 1
                except Exception:
                    stat['numberOfVisits'] = 1
                jsonFile = open('data.json', 'w')
                jsonFile.write(json.dumps(stats, ensure_ascii=True))
                jsonFile.close()
                return jsonify(stat)
            else:
                continue
        return jsonify({
            'message': 'uniqueID not found in database'
        })


if __name__ == '__main__':
    app.run(debug=True)
