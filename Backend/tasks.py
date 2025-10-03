from .celery_app import make_celery
from . import create_app, db
from .parser import parse_resume
from .models import Candidate

app = create_app()
celery = make_celery(app)

@celery.task(bind=True)
def parse_resume_task(self, filepath, filename):
	parsed = parse_resume(filepath)
	# map parsed fields to our Candidate model
	cand = Candidate(
		name=parsed.get('name'),
		email=parsed.get('email'),
		phone=parsed.get('phone'),
		education=parsed.get('education'),
		skills=parsed.get('skills'),
		experience_years=parsed.get('experience_years'),
		full_text=parsed.get('full_text'),
		raw_file_url=filename,
		metadata={'source_path': filepath}
	)
	db.session.add(cand)
	db.session.commit()
	return {'candidate_id': cand.id}
 