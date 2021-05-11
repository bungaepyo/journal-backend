from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Journal(db.Model):
    ___tablename___ = "journal"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", cascade="delete")

    def ___init___(self, **kwargs):
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.date = kwargs.get("date")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "tasks": [t.serialize() for t in self.tasks]
        }

class Task(db.Model):
    ___tablename___ = "task"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    journal_id = db.Column(db.Integer, db.ForeignKey("journal.id"))

    def ___init___(self, **kwargs):
        self.description = kwargs.get("description")
        self.done = kwargs.get("done")
        self.journal_id = kwargs.get("journal_id")

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done
        }