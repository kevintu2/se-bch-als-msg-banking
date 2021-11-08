# app.py

# Required imports
import os 
from flask import Flask, request, jsonify
from google.cloud import firestore
from google.cloud import storage
import uuid

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
db = firestore.Client()
todo_ref = db.collection('todos')

#Initialize Cloud Storage
#CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
CLOUD_STORAGE_BUCKET_NAME = "als-audio-bucket"
storage_client = storage.Client()
bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET_NAME)


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
def upload_audio():
    destination_file_name = f'Audio{uuid.uuid1()}.wav'
    blob = bucket.blob(destination_file_name)
    fileName = request.json['fileName']

    blob.upload_from_filename(fileName)

    return  "File {} uploaded to {}.".format(
            fileName, destination_file_name
        )
@app.route('/retrieve_audio', methods=['GET'])
def retrieve_audio():
    fileName = request.json['fileName']
    destination_file_name = "download.wav"
    blob = bucket.blob(fileName)
    blob.download_to_filename(destination_file_name)

    return "Downloaded storage object {} from bucket {} to local file {}.".format(
            fileName, CLOUD_STORAGE_BUCKET_NAME, destination_file_name
        )


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)