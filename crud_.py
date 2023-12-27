from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


app = FastAPI()

db_url = "postgresql://Alla:2002@localhost:5432/Exam"
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)

class MySession(BaseModel):
    id: int
    Professor: str
    DateSession: Date
    ControlType: str
    GroupId: int
    SubId: int

class Group(BaseModel):
    id: int
    Faculty: str
    GroupCode: str
    Course: int
    StudentsNum: int
    

class Subject(BaseModel):
    id: int
    Name: str
    Hours: int
    Department: str
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD операции
@app.post("/sessions/", response_model=dict)
def create_session(session: MySession, db: Session = Depends(get_db)):
    db.add(session)
    db.commit()
    db.refresh(session)
    return session.dict()

@app.get("/sessions/{session_id}", response_model=dict)
def read_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(MySession).filter(MySession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.dict()

@app.put("/sessions/{session_id}", response_model=dict)
def update_session(session_id: int, new_data: MySession, db: Session = Depends(get_db)):
    session = db.query(MySession).filter(MySession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    for key, value in new_data.dict().items():
        setattr(session, key, value)
    db.commit()
    db.refresh(session)
    return session.dict()

@app.delete("/sessions/{session_id}", response_model=dict)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(MySession).filter(MySession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}
# CRUD операции для Group
@app.post("/groups/", response_model=dict)
def create_group(group: Group, db: Session = Depends(get_db)):
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@app.get("/groups/{group_id}", response_model=dict)
def read_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@app.put("/groups/{group_id}", response_model=dict)
def update_group(group_id: int, new_data: Group, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    for key, value in new_data.dict().items():
        setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return group

@app.delete("/groups/{group_id}", response_model=dict)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}

# CRUD операции для Subject
@app.post("/subjects/", response_model=dict)
def create_subject(subject: Subject, db: Session = Depends(get_db)):
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

@app.get("/subjects/{subject_id}", response_model=dict)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@app.put("/subjects/{subject_id}", response_model=dict)
def update_subject(subject_id: int, new_data: Subject, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in new_data.dict().items():
        setattr(subject, key, value)
    db.commit()
    db.refresh(subject)
    return subject

@app.delete("/subjects/{subject_id}", response_model=dict)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted successfully"}

#join
@app.get("/sessions/{session_id}/details", response_model=dict)
def get_session_details(session_id: int, db: Session = Depends(get_db)):
    session = db.query(MySession).filter(MySession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    group = db.query(Group).filter(Group.id == session.GroupId).first()
    subject = db.query(Subject).filter(Subject.id == session.SubId).first()

    return {"session": session.dict(), "group": group.dict(), "subject": subject.dict()}

#update
@app.put("/sessions/{session_id}/update-professor", response_model=dict)
def update_session_professor(session_id: int, new_professor: str, db: Session = Depends(get_db)):
    session = db.query(MySession).filter(MySession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.Professor != "Bob":
        session.Professor = new_professor
        db.commit()
        db.refresh(session)
        return session.dict()
    else:
        raise HTTPException(status_code=400, detail="Cannot update professor for this session.")
#group by
from sqlalchemy import func

@app.get("/sessions/group-by-professor", response_model=list)
def group_sessions_by_professor(db: Session = Depends(get_db)):
    result = (
        db.query(MySession.Professor, func.count().label("sessions_count"))
        .group_by(MySession.Professor)
        .all()
    )
    return result
  
#sort
from sqlalchemy import desc

@app.get("/sessions/sorted-by-date", response_model=list)
def get_sessions_sorted_by_date(db: Session = Depends(get_db)):
    sessions = db.query(MySession).order_by(desc(MySession.DateSession)).all()
    return sessions

#select
from fastapi import Query

@app.get("/groups/", response_model=list)
def get_groups_with_conditions(
    faculty: str = Query(None, title="Faculty name", description="Filter by faculty name"),
    group_code: str = Query(None, title="Group code", description="Filter by group code"),
    course: int = Query(None, title="Course", description="Filter by course"),
    students_num: int = Query(None, title="Number of students", description="Filter by number of students"),
    db: Session = Depends(get_db)
):
    conditions = []
    if faculty:
        conditions.append(Group.Faculty == faculty)
    if group_code:
        conditions.append(Group.GroupCode == group_code)
    if course:
        conditions.append(Group.Course == course)
    if students_num:
        conditions.append(Group.StudentsNum == students_num)

    conditions = and_(*conditions)

    if not conditions:
        raise HTTPException(status_code=400, detail="At least one filter condition is required.")

    try:
        groups = db.query(Group).filter(conditions).all()
        return groups
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving groups: {str(e)}")

