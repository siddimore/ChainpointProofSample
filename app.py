import requests
from flask import Flask, redirect, request, jsonify

#from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/proof/', methods=['POST'])
def getProof():
    values = request.get_json()
    print (values)
    # Check that the required fields are in the POST'ed data
    required = ['nodeId']
    if not all(k in values for k in required):
        return 'Missing Hash', 400

    res = requests.get('http://35.230.179.171/proofs/' + values['nodeId'])
    print ((res.status_code))
    print(res.content)

    return res.content, 200

@app.route('/SubmitHash/new', methods=['POST'])
def hashSubmit():
    values = request.get_json()
    print (values)

    # Check that the required fields are in the POST'ed data
    required = ['hashes']
    if not all(k in values for k in required):
        return 'Missing Hash', 400

    res = requests.post('http://35.230.179.171/hashes', json=values)
    print ((res.status_code))
    print(res.content)

    return res.content, 200

if __name__ == '__main__':
    app.run()
