# app.py

# Required imports
import uuid
from google.cloud import storage
import os
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import google.auth.transport.requests
from google.oauth2 import id_token
from functools import wraps

from pyasn1.type.univ import Null

HTTP_REQUEST = google.auth.transport.requests.Request()

# Initialize Flask app
from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize Firestore DB
db = firestore.Client()
users_collection = db.collection('users')
user = None

# Initialize Cloud Storage
#CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
CLOUD_STORAGE_BUCKET_NAME = "als-audio-bucket"
storage_client = storage.Client.from_service_account_json(
    'serviceaccount.json')
bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET_NAME)


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_header = request.headers['Authorization']
        if not auth_header:
            return {'message': 'No token provided'}, 400
        idtoken = auth_header.split(' ').pop()
        claims = id_token.verify_firebase_token(
            idtoken, HTTP_REQUEST, audience=os.environ.get('GOOGLE_CLOUD_PROJECT'))
        if not claims:
            return 'Unauthorized', 401
        return f(*args, **kwargs)
    return wrap


@app.route('/register', methods=['POST'])
@check_token
def register():
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    auth_header = request.headers['Authorization']
    idtoken = auth_header.split(' ').pop()
    claims = id_token.verify_firebase_token(
        idtoken, HTTP_REQUEST, audience=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    user_ref = users_collection.document(claims['sub'])
    user_snapshot = user_ref.get()
    if user_snapshot.exists:
        return {'message': 'User already exists'}, 400
    user_ref.set(data)
    return {'message': 'User created successfully'}, 200


@app.route('/login', methods=['GET'])
@check_token
def login():
    return {'message': 'Successfully logged in'}, 200


@app.route('/upload_audio', methods=['POST'])
@check_token
def upload_audio():
    destination_file_name = f'Audio{uuid.uuid1()}.wav'
    # print('request.files', request.files)
    file = request.files['file']
    fileName = file.name
    print(file)
    blob = bucket.blob(destination_file_name)

    blob.upload_from_string(file.read(), content_type=file.content_type)
    auth_header = request.headers['Authorization']
    idtoken = auth_header.split(' ').pop()
    claims = id_token.verify_firebase_token(
        idtoken, HTTP_REQUEST, audience=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    user_ref = users_collection.document(claims['sub'])
    doc = user_ref.get()
    if doc.exists:
        doc = doc.to_dict()
        print(doc)
        if "audio" in doc:
            doc["audio"].append({fileName: destination_file_name})
            user_ref.update({"audio": doc["audio"]})
        else:
            user_ref.update({"audio": [{fileName: destination_file_name}]})
    else:
        print(u'No such document!')
    return "File {} uploaded to {}.".format(
        fileName, destination_file_name
    )


@app.route('/retrieve_audio', methods=['POST'])
def retrieve_audio():
    fileName = request.json['fileName']
    blob = bucket.blob(fileName)

    url = blob.generate_signed_url(version="v4",
                                   # This URL is valid for 15 minutes
                                   expiration=datetime.timedelta(minutes=30),
                                   # Allow GET requests using this URL.
                                   method="GET",)
    # blob.download_to_filename(destination_file_name)
    print("Generated GET signed URL:")
    return url


@app.route('/display_audio', methods=['GET'])
def display_audio():
    data = user_ref.get()
    print("Grabbed User audios")
    if data.audio:
        #format is [{userFileName:blobStoreFileName}]
        return data.audio
    else:
        return []


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
