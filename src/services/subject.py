import models.models as _models
from configs.database import db_dependency
from fastapi import HTTPException
from models.schema import SubjectSchema


async def save_subject(subject: SubjectSchema, db: db_dependency):
    db_subject = _models.Subject(name=subject.name, thumbnail=subject.thumbnail)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    print(db_subject)
    
    return db_subject

async def get_subjects_service(db: db_dependency):
    subjects = db.query(_models.Subject).all()
    subject_dicts = [subject_to_dict(subject) for subject in subjects]
    return subject_dicts

async def get_subject_by_id(subject_id: str, db: db_dependency):
    db_subject = db.query(_models.Subject).filter(_models.Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject_to_dict(db_subject)

def subject_to_dict(subject):
    return {
        "id": subject.id,
        "name": subject.name,
        "thumbnail": subject.thumbnail,
    }

