import os
from flask import Flask, request, jsonify
from flask_cors import CORS 
from .models import db, Candidate
from .celery_app import make_celery

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register blueprints
    from . import routes
    app.register_blueprint(routes.bp)

    return app

app = create_app()
celery = make_celery(app)

@app.route('/resumes/upload', methods=['POST'])
def upload_resume():
    from .tasks import parse_resume_task  # <-- MOVED IMPORT
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    task = parse_resume_task.delay(filepath, file.filename)
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(debug=True)