import json
import os
from flask import request, Flask
from datetime import datetime
from db import Journal, Task, db

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

#### Journal Routes ####

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
@app.route("/journals/<int:journal_id>/", methods=["DELETE"])
def delete_journal_by_id(journal_id):
    journal = Journal.query.filter_by(id = journal_id).first()
    if journal is None:
        return failure_response("Journal not found")
    db.session.delete(journal)
    db.session.commit()
    return success_response(journal.serialize())

# 5: Update a journal
@app.route("/journals/<int:journal_id>/", methods=["POST"])
def update_journal_by_id(journal_id):
    body = json.loads(request.data)
    title = body.get("title")
    description = body.get("description")

    journal = Journal.query.filter_by(id = journal_id).first()
    if title is not None:
        journal.title = title
    if description is not None:
        journal.description = description
    db.session.commit()
    return success_response(journal.serialize())

#### Task Routes ####

# 1: Create task for a specific journal
@app.route("/journals/<int:journal_id>/tasks/", methods=["POST"])
def create_task(journal_id):
    journal = Journal.query.filter_by(id = journal_id).first()
    if journal is None:
        return failure_response("Journal not found")
    
    body = json.loads(request.data)
    description = body.get("description")
    if description is None:
        return failure_response("No description provided")

    new_task = Task(
        description = description,
        done = body.get("done", False),
        journal_id = journal_id
    )
    db.session.add(new_task)
    db.session.commit()
    return success_response(new_task.serialize())

# 2: Update task by id
@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task_by_id(task_id):
    body = json.loads(request.data)
    description = body.get("description")
    done = body.get("done")

    task = Task.query.filter_by(id = task_id).first()
    if task is None:
        return failure_response("Task not found")
    if description is not None:
        task.description = description
    if done is not None:
        task.done = done
    db.session.commit()
    return success_response(task.serialize())

# 3: Delete task by id
@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = Task.query.filter_by(id = task_id).first()
    if task is None:
        return failure_response("Task not found")
    db.session.delete(task)
    db.session.commit()
    return success_response(task.serialize())

# 4: Get all tasks of a specific journal
@app.route("/journals/<int:journal_id>/tasks/")
def get_tasks_of_journal(journal_id):
    journal = Journal.query.filter_by(id = journal_id).first()
    if journal is None:
        return failure_response("Journal not found")
    
    return success_response(journal.serialize()["tasks"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)