from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Journal(db.Model):
    ___tablename___ = "journal"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    def ___init___(self, **kwargs):
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.date = kwargs.get("date")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date
        }