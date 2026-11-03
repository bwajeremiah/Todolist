
from backend import notesFormat
from pymongo import MongoClient
import json
import time
from .notesFormat import Note
from flask import Flask, jsonify,request
app = Flask(__name__)
uri = "mongodb+srv://bwajeremiah_db_user:39firehouse@cluster0.hklay79.mongodb.net/"
client = MongoClient(uri)

try:
    database = client.get_database("NotesApp")
    notes = database.get_collection("notes")
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)
@app.get("/api/notes/")
def list_notes():
    all_notes = notes.find()
    return jsonify([Note(note["text"], note["id"], note["last_edited_date"]).to_dict() for note in all_notes])
@app.get("/api/notes/count")
def get_note_count():
    count = notes.count_documents({})
    return jsonify({"count": count})
@app.post("/api/notes")
def add_note():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    data = request.get_json()
    new_note = {
        "text": data.get("text"),
        "id": notes.count_documents({}) + 1,
        "last_edited_date": current_time
    }
    notes.insert_one(new_note)
    return jsonify(new_note)
@app.delete("/api/notes/<int:id>")
def deleteNote(id):
    result = notes.delete_one({"id": id})
    if result.deleted_count == 0:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"message": "Note deleted successfully"})
@app.patch("/api/notes/edit")
def edit_note():
    data = request.get_json()
    note_id = data.get("id")
    new_text = data.get("text")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    result = notes.update_one(
        {"id": note_id},
        {"$set": {"text": new_text, "last_edited_date": current_time}}
    )
    if result.modified_count == 0:
        return jsonify({"error": "Note not found"}), 404
    updated_note = notes.find_one({"id": note_id})
    return jsonify(updated_note)
def main() -> None:
    app.run(debug=True, port=8000)

