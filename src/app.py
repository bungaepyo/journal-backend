import json
import os
from flask import request, Flask
from datetime import datetime
from db import Journal, db

app = Flask(__name__)
db_filename = "journal.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# 1: Get all journals
@app.route("/")
@app.route("/journals/")
def get_all_journals():
    return success_response([j.serialize() for j in Journal.query.all()])

# 2: Get journal by ID
@app.route("/journals/<int:journal_id>/")
def get_journal_by_id(journal_id):
    journal = Journal.query.filter_by(id = journal_id).first()
    if journal is None:
        return failure_response("Journal not found")
    return success_response(journal.serialize())

# 3: Create a journal
@app.route("/journals/", methods=["POST"])
def create_journal():
    body = json.loads(request.data)
    title = body.get("title")
    if title is None:
        return failure_response("No title provided")
    description = body.get("description")
    if description is None:
        return failure_response("No description provided")
    date = datetime.now()
    new_journal = Journal(title = title, description = description, date = date)
    db.session.add(new_journal)
    db.session.commit()
    return success_response(new_journal.serialize(), 201)

# 4: Delete a journal


# 4: Update a journal

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)