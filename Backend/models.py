from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func

db = SQLAlchemy()

class Candidate(db.Model):
	__tablename__ = 'candidates'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, index=True)
	email = db.Column(db.String, index=True)
	phone = db.Column(db.String)
	education = db.Column(JSONB)
	skills = db.Column(JSONB)
	experience_years = db.Column(db.Float)
	full_text = db.Column(db.Text)
	raw_file_url = db.Column(db.String)
	metadata = db.Column(JSONB)
	created_at = db.Column(db.DateTime, server_default=func.now())

