from flask import Flask
from app.extensions import db
from app.models.job import Job 
from app.routes.jobs import jobs_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return {"message": "Job Tracker API is running"}
    
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "An unexpected error occurred"}, 500
    
    app.register_blueprint(jobs_bp)
    
    return app