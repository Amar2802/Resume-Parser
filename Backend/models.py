from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy import func, event

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
    candidate_metadata = db.Column(JSONB)
    created_at = db.Column(db.DateTime, server_default=func.now())
    search_vector = db.Column(TSVECTOR)

# SQL to create the trigger
trigger_sql = """
CREATE OR REPLACE FUNCTION candidates_search_vector_update() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        to_tsvector('pg_catalog.english', coalesce(NEW.name, '')) ||
        to_tsvector('pg_catalog.english', coalesce(NEW.email, '')) ||
        to_tsvector('pg_catalog.english', array_to_string(NEW.skills, ' ')) ||
        to_tsvector('pg_catalog.english', coalesce(NEW.full_text, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON candidates FOR EACH ROW EXECUTE PROCEDURE candidates_search_vector_update();
"""

# Use event.listen to execute the SQL after the table is created
event.listen(Candidate.__table__, 'after_create', db.DDL(trigger_sql))

