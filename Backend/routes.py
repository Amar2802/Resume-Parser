from flask import request, jsonify
from sqlalchemy import func
from .models import Candidate  # make sure Candidate model is imported
from . import bp  # your Flask blueprint

@bp.route('/resumes/search')
def search():
    q = request.args.get('q')  # free text
    skill = request.args.get('skill')
    min_exp = request.args.get('min_exp', type=float)

    base = Candidate.query

    if skill:
        # skills stored as lowercased strings in JSONB array
        base = base.filter(Candidate.skills.contains([skill.lower()]))

    if min_exp is not None:
        base = base.filter(Candidate.experience_years >= min_exp)

    if q:
        # plainto_tsquery is safer than to_tsquery for free-text input
        tsq = func.plainto_tsquery('english', q)
        base = base.filter(Candidate.search_vector.op('@@')(tsq))

        # OR if using SQLAlchemy full text search extension:
        # base = base.filter(Candidate.search_vector.match(q, postgresql_regconfig='english'))

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
