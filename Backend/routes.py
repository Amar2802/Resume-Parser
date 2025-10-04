from flask import request, jsonify, Blueprint # <-- IMPORT BLUEPRINT
from sqlalchemy import func
from .models import Candidate

bp = Blueprint('api', __name__) # <-- CREATE THE BLUEPRINT

@bp.route('/resumes/search')
def search():
    q = request.args.get('q')
    skill = request.args.get('skill')
    min_exp = request.args.get('min_exp', type=float)

    base = Candidate.query

    if skill:
        base = base.filter(Candidate.skills.contains([skill.lower()]))

    if min_exp is not None:
        base = base.filter(Candidate.experience_years >= min_exp)

    if q:
        tsq = func.plainto_tsquery('english', q)
        base = base.filter(Candidate.search_vector.op('@@')(tsq))

    results = (
        base.order_by(Candidate.created_at.desc())
        .limit(50)
        .all()
    )

    return jsonify([
        {
            'id': r.id,
            'name': r.name,
            'email': r.email,
            'skills': r.skills,
            'experience_years': r.experience_years
        }
        for r in results
    ])