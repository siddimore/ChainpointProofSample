import requests
import hashlib
import os
import uuid
import json
from flask import Flask, redirect, request, jsonify, render_template
from werkzeug import secure_filename

#from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/proof/', methods=['GET'])
def getProofFromNode():
    #values = request.get_json()
    nodeId = request.args.get('nodeId')
    print (nodeId)
    # Check that the required fields are in the POST'ed data
    required = ['nodeId']
    if nodeId is None:
        return 'Missing NodeId', 400

    res = requests.get('http://35.230.179.171/proofs/' + nodeId)
    print ((res.status_code))
    print(res.content)
    # return render_template('upload.html', filehash = res.content["meta"])

    return res.content, 200

@app.route('/upload')
def upload_file():
   return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        extension = os.path.splitext(f.filename)[1]

        f_name = str(uuid.uuid4()) + extension
        f.save(secure_filename(f_name))

        fileHash = getFileHash(f_name)
        print (fileHash)
        hashArray = []
        hashArray.append(fileHash)
        jsonFileHash = {'hashes':hashArray}

        hashNode, hash, retCode = chainPointHash(jsonFileHash)
        #print(jsonify(content))
        #return json.dumps({'fileHash':fileHash})
        return render_template('upload.html', nodeId = hashNode, filehash = hash)
        #return content, retCode


@app.route('/getDocProof', methods=['POST'])
def getDocProof():
    nodeId = request.form['node_id']
    print (nodeId)
    # # Check that the required fields are in the POST'ed data
    # required = ['nodeId']
    # if not all(k in values for k in required):
    #     return 'Missing Hash', 400

    res = requests.get('http://35.230.179.171/proofs/' + nodeId)
    data = res.json()
    print(data)
    for entry in data:
        print(entry['proof'])
        chaipointProof = entry['proof']

    return render_template('upload.html', proof = chaipointProof)
    #
    # return res.content, 200


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

    data = res.json()
    proof = data.get('proof')

    return proof, 200

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

    # return res.content, 200

def docProof(proof):

    res = requests.get('http://35.230.179.171/proofs/' + proof)
    print ((res.status_code))
    print(res.content)

    return res.content, 200

def chainPointHash(fileHash):
    print(fileHash)
    res = requests.post('http://35.230.179.171/hashes', json=fileHash)
    print ((res.status_code))
    data = res.json()
    meta = data.get('meta')
    hashes = data.get('hashes')
    print((hashes[0]['hash_id_node']))
    print((hashes[0]['hash']))
    # output = json.dumps(res.content)
    #
    # # Convert bytes to string type and string type to dict
    # print("resp: " + output)
    # print(output["meta"])
    # string = res.read().decode('utf-8')
    # json_obj = json.loads(string)
    # print(json_obj)

    return hashes[0]['hash_id_node'], hashes[0]['hash'], 200

def getFileHash(filename):

    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    print(sha256_hash.hexdigest())
    return sha256_hash.hexdigest()


if __name__ == '__main__':
    app.run()
