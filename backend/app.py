# app.py

# Required imports
import uuid
from google.cloud import storage
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import google.auth.transport.requests
from google.oauth2 import id_token
from functools import wraps

from pyasn1.type.univ import Null

HTTP_REQUEST = google.auth.transport.requests.Request()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
db = firestore.Client()
users_collection = db.collection('users')
user = None

# Initialize Cloud Storage
#CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
CLOUD_STORAGE_BUCKET_NAME = "als-audio-bucket"
storage_client = storage.Client()
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


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/upload_audio', methods=['POST'])
@check_token
def upload_audio():
    destination_file_name = f'Audio{uuid.uuid1()}.wav'
    # print('request.files', request.files)
    file = request.files['file']
    fileName  = file.name
    print(file)
    blob = bucket.blob(destination_file_name)

    blob.upload_from_string(file.read(),content_type=file.content_type)
    auth_header = request.headers['Authorization']
    idtoken = auth_header.split(' ').pop()
    claims = id_token.verify_firebase_token(
        idtoken, HTTP_REQUEST, audience=os.environ.get('GOOGLE_CLOUD_PROJECT'))
    user_ref = users_collection.document(claims['sub'])
    doc = user_ref.get()
    if doc.exists:
        doc =  doc.to_dict()
        print(doc)
        if "audio" in doc:
            doc["audio"].append({fileName:destination_file_name})
            user_ref.update( { "audio" : doc["audio"] })
        else:
            user_ref.update({ "audio":[{fileName:destination_file_name}]})
    else:
        print(u'No such document!')
    return "File {} uploaded to {}.".format(
        fileName, destination_file_name
    )

@app.route('/retrieve_audio', methods=['GET'])
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
