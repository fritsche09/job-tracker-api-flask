# Job Tracker API 

## Description

A REST API for tracking job applications built with Flask, SQLAlchemy, and Marshmallow. Supports full CRUD operations create, read, update, and delete job applications via JSON endpoints. 

## Tech Stack

- Python
- Flask 
- SQLAlchemy
- Marshmallow 
- PostgreSQL

## How To Run Locally

1. Clone the repository
```bash
   git clone https://github.com/fritsche09/job-tracker-api-flask.git
   cd job-tracker-api-flask
```

2. Create and activate a virtual environment
```bash
   python3 -m venv .venv
   source .venv/bin/activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`

5. Set up a PostgreSQL database and update your `.env` file
   - Create a new database in PostgreSQL 
   - Update your `.env` with your database credentials:
```
   SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/your-database-name
```

6. Run the app
```bash
   python run.py
```


## Endpoints

|           | GET                       | POST                             | PUT                  | DELETE             |
|-----------|---------------------------|----------------------------------|----------------------|------------        |
|jobs/      | Returns a list of all jobs|  Creates and saves a new job     |  N/A                 |  N/A               |
|/jobs/\<id>| Returns a job by its id   |  N/A                             |  Updates job by id   |  Deletes job by id |

## Model 
This code creates a `Job` model with the following attributes:
```python
from app.extensions import db
from datetime import date

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="applied")
    applied_date = db.Column(db.Date, default=date.today)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Job {self.company} - {self.role}>"
```

## Schema 
It also uses Marshmallow for data serialization

```python
from marshmallow import Schema, fields, validate

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    company = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    role = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    status = fields.Str(load_default="applied")
    applied_date = fields.Date(load_default=None)
    notes = fields.Str(load_default=None)
```

## Example requests for POST & PUT endpoints

### /jobs body (POST):

```json
{
    "applied_date": "2026-03-17",
    "company": "XYZ",
    "notes": "Interview went well",
    "role": "Engineering",
    "status": "Applied"
}
```
### Server response:
```json
{
    "message": "Job has been posted"
}
```
status code: `201 CREATED`

### /jobs/\<id> body (PUT):
```json
{
    "notes": "Made it to the second round of interviews"
}
```

### Server response:

```json
{
    "applied_date": "2026-03-17",
    "company": "XYZ",
    "id": 3,
    "notes": "Made it to the second round of interviews",
    "role": "Engineering",
    "status": "Applied"
}
```
status code: `200 OK`


