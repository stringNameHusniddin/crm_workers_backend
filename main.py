from fastapi import Depends, FastAPI, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, hashing, tokin, oauth2
from database import get_db, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WORK CRUD 

@app.get('/work', tags=["Work"], response_model=list[schemas.ShowWorks])
def getWork(session: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    work = session.query(models.WorksModel).all()
    return work

@app.post("/work", tags=["Work"])
def CreateWork(work: schemas.WorksSchema, session: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    work = models.WorksModel(name=work.name, join_data=work.join_data, complete_data=work.complete_data, status=work.status, owner_id=work.owner_id, to_id=work.to_id)
    session.add(work)
    session.commit()
    session.refresh(work)
    return work

@app.put("/work/{id}", tags=["Work"])
def updateWork(id: int, work: schemas.WorksSchema, session: Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    workObject = session.query(models.WorksModel).get(id)
    workObject.name = work.name
    workObject.join_data = work.join_data
    workObject.complete_data = work.complete_data
    workObject.status = work.status
    workObject.to_id = work.to_id
    workObject.owner_id = work.owner_id
    session.commit()
    return work

@app.delete("/work/{id}", tags=["Work"])
def deleteWork(id: int, session: Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    workObject = session.query(models.WorksModel).get(id)
    session.delete(workObject)
    session.commit()
    session.close()
    return "Item was deleted..."


# USER

@app.get("/user/{username}", tags=["User"], response_model=schemas.ShowUser)
def detail_user(username:str, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    user = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    
    return user

@app.get("/user", tags=["User"], response_model=list[schemas.ShowUser])
def getUser(session: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    users = session.query(models.UserModel).all()
    return users

@app.post("/user", tags=["User"])
def CreateUser(user: schemas.UserSchema, session: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    user = models.UserModel(role=user.role, username=user.username, password=hashing.Hash.bcrypt(user.password), first_name=user.first_name, last_name=user.last_name, join_data=user.join_data, status=user.status, age=user.age, email=user.email, boss_id=user.boss_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.put("/user/{id}", tags=["User"])
def updateUser(id: int, user: schemas.UserSchema, session: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    userObject = session.query(models.UserModel).filter(models.UserModel.id == id)
    if not userObject.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    userObject.update(user.dict())
    session.commit()
    return user

@app.delete("/user/{id}", tags=["User"])
def deleteUser(id: int, session: Session = Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    workObject = session.query(models.UserModel).get(id)
    session.delete(workObject)
    session.commit()
    session.close()
    return "Item was deleted..."


# AUTH 

@app.post('/login', tags=["Auth"]) 
def login(request: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = session.query(models.UserModel).filter(models.UserModel.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid username")
    if not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=f"Incorrect password")

    access_token = tokin.create_access_token(data={"sub":user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# NOTES 

@app.get("/notes", tags=["notes"], response_model=list[schemas.ShowNote])
def list_notes(db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    notes = db.query(models.NoteModel).all()
    return notes

@app.get("/notes/{id}", tags=["notes"], response_model=schemas.ShowNote)
def detail_notes(id:int, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == id).first()
    return note

@app.post("/notes", tags=["notes"], response_model=schemas.ShowNote)
def create_notes(req:schemas.Note, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    new_note = models.NoteModel(text=req.text, owner_id=req.owner_id)

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@app.delete("/notes/{id}", tags=["notes"])
def delete_user(id:int, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    note = db.query(models.NoteModel).filter(models.NoteModel.id == id)
    if not note.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    note.delete()
    db.commit()
    return "done"

# Notifications

@app.post("/notifications", tags=["notifications"])
def create_notifications(req:schemas.createNotifications, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    new_notification = models.Notification(text = req.text, owner_id = req.owner_id, to_id = req.to_id)
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification

@app.get("/notifications", tags=["notifications"])
def list_notifications(db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    notifications = db.query(models.Notification).all()

    return notifications

@app.put("/notifications/{id}", tags=["notifications"])
def update_notifications(id:int, req:schemas.createNotifications, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    notification =db.query(models.Notification).filter(models.Notification.id == id)
    if not notification.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    notification.update(dict(req))
    db.commit()
    return notification

@app.delete("/notifications/{id}", tags=["notifications"])
def delete_notifications(id:int, db:Session=Depends(get_db), current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    notification =db.query(models.Notification).filter(models.Notification.id == id)
    if not notification.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    notification.delete()
    db.commit()
    return notification