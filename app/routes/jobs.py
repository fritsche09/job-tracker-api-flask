from flask import Blueprint, request
from app.models.job import Job
from app.extensions import db
from app.schemas.job import JobSchema
from marshmallow import ValidationError


jobs_bp = Blueprint("jobs", __name__)
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    all_jobs = Job.query.all()
    result = jobs_schema.dump(all_jobs)
    return result, 200

@jobs_bp.route("/jobs/<id>", methods=["GET"])
def get_job(id):
    requested_job = db.session.get(Job, id)
    if requested_job:
        return job_schema.dump(requested_job), 200
    
    return {"error": "Job not found"}, 404

@jobs_bp.route("/jobs", methods=["POST"])
def post_jobs():
    new_job = request.get_json()

    try:
        deserialized_job = job_schema.load(new_job)
        job_object = Job(**deserialized_job)

        db.session.add(job_object)
        db.session.commit()
        return {"message": "Job has been posted"}, 201
    except ValidationError as e:
        return {"error": e.messages}, 400

@jobs_bp.route("/jobs/<id>", methods=["PUT"])
def update_jobs(id):
    current_job = db.session.get(Job, id)
    
    if not current_job:
        return {"error": "Job not found"}, 404
    
    
    try:
        updated_job = job_schema.load(request.get_json(), partial=True)
        for key, value in updated_job.items():
            setattr(current_job, key, value)

        db.session.commit()
        
        return job_schema.dump(current_job), 200
    except ValidationError as e:
        return {"error": e.messages}, 400

@jobs_bp.route("/jobs/<id>", methods=["DELETE"])
def delete_job(id):
    job_to_delete = db.session.get(Job, id)

    if not job_to_delete:
        return {"message": "No job to delete or job doesn't exist"}, 404
    
    db.session.delete(job_to_delete)
    db.session.commit()

    return "", 204

    


