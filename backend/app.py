# app.py

# Required imports
from flask_cors import CORS, cross_origin
from flask import Flask
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
from audio import processAudio

from pyasn1.type.univ import Null
import sys

HTTP_REQUEST = google.auth.transport.requests.Request()

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize Firestore DB
db = firestore.Client()
users_collection = db.collection('users')

# Initialize Cloud Storage
CLOUD_STORAGE_BUCKET_NAME = "als-audio-bucket3"
storage_client = storage.Client.from_service_account_json(
    'serviceaccount.json')
bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET_NAME)


# Helper function to check the user's token


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

# Register a new user


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

# "Login" a user


@app.route('/login', methods=['GET'])
@check_token
def login():
    return {'message': 'Successfully logged in'}, 200

# Upload Audio


@app.route('/upload_audio', methods=['POST'])
@check_token
def upload_audio():
    destination_file_name = f'Audio{uuid.uuid1()}.wav'
    file = request.files['file']
    fileName = file.filename
    blob = bucket.blob(destination_file_name)
    
    blob.upload_from_string(file.read(), content_type=file.content_type)
    
    # tmp folder for processed audio files
    file_path = '/tmp/' + str(fileName)
    blob.download_to_filename(file_path)
    processedFilePaths = processAudio(file_path)

    firebaseEntries = []

    unique_folder="Folder "+str(uuid.uuid1()) #generates a unique folder id for all the chunks the audio file will be split into
    
    # uploads processed audio files to new blobs
    for path in processedFilePaths:
        dest_processed_file = f'Audio{uuid.uuid1()}.wav'
        processedFileName = path.split('/tmp/')[1]
        firebaseEntries.append((processedFileName, dest_processed_file, unique_folder))

        blob = bucket.blob(dest_processed_file)
        blob.upload_from_filename(path, content_type='audio/wav')
    

    auth_header = request.headers['Authorization']
    idtoken = auth_header.split(' ').pop()
    claims = id_token.verify_firebase_token(
        idtoken, HTTP_REQUEST, audience=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    user_ref = users_collection.document(claims['sub'])

    doc = user_ref.get()
    if doc.exists:        
        doc = doc.to_dict()

        # uploads each processed file name/path to firebase
        for (procfileName, destprocFile, folderid) in firebaseEntries:
            if "audio" in doc:
                doc["audio"].append({(procfileName): (destprocFile,folderid)})
                user_ref.update({"audio": doc["audio"]})
            else:
                user_ref.update({"audio": [{(procfileName): (destprocFile,folderid)}]})
                doc = user_ref.get()
                doc = doc.to_dict()

    else:
        print(u'No such document!')
    
    if len(processedFilePaths) == 0:
        return "No processed files to upload"
    else:
        fileNames, destFiles, folderid = zip(*firebaseEntries)
        return "Files {} uploaded to {} in folder {}.".format(fileNames, destFiles, folderid)

# Get Audio


@app.route('/retrieve_audio', methods=['POST'])
def retrieve_audio():
    fileName = request.json['fileName']
    blob = bucket.blob(fileName)

    url = blob.generate_signed_url(version="v4",
                                   # This URL is valid for 30 minutes
                                   expiration=datetime.timedelta(minutes=30),
                                   # Allow GET requests using this URL.
                                   method="GET",)
    print("Generated GET signed URL:")
    return url


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)