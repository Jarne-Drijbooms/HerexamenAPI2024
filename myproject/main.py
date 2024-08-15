from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import auth
import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_speler(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT 
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/spelers/me", response_model=schemas.Player)
def read_spelers_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_player = auth.get_current_active_player(db, token)
    return current_player

@app.post("/spelers/", response_model=schemas.Player)
def maak_speler(speler: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_speler = crud.get_player_by_email(db, email=speler.email)
    if db_speler:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, speler=speler)


@app.get("/spelers/", response_model=list[schemas.Player])
def lees_spelers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spelers = crud.get_player(db, skip=skip, limit=limit)
    return spelers


@app.get("/spelers/{speler_id}", response_model=schemas.Player)
def lees_speler(speler_id: int, db: Session = Depends(get_db)):
    db_speler = crud.get_player(db, speler_id=speler_id)
    if db_speler is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return db_speler

@app.put("/spelers/{speler_id}", response_model=schemas.Player)
def update_speler(speler_id: int, speler: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.update_player(db=db, speler=speler, speler_id=speler_id)

@app.delete("/spelers/{speler_id}")
def verwijder_speler(speler_id: int, db: Session = Depends(get_db)):
    crud.delete_player(db=db, speler_id=speler_id)
    return {"message": f"succesvol verwijderd speler met id: {speler_id}"}

@app.post("/spelers/{speler_id}/compititie/", response_model=schemas.Compititie)
def maak_compititie_voor_speler(
    speler_id: int, compititie: schemas.CompititieCreate, db: Session = Depends(get_db)
):
    return crud.maak_speler_compititie(db=db, compititie=compititie, speler_id=speler_id)


@app.get("/compititie/", response_model=list[schemas.Compititie])
def lees_compititie(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    compititie = crud.get_compititie(db, skip=skip, limit=limit)
    return compititie


@app.delete("/compititie/{compititie_id}")
def verwijder_compititie(compititie_id: int, db: Session = Depends(get_db)):
    crud.verwijder_compititie(db=db, compititie_id=compititie_id)
    return {"message": f"succesvol verwijderd compititie met id: {compititie_id}"}

@app.post("/spelers/{speler_id}/beker/", response_model=schemas.Beker)
def maak_beker_voor_speler(
    speler_id: int, beker: schemas.BekerCreate, db: Session = Depends(get_db)
):
    return crud.maak_speler_beker(db=db, beker=beker, speler_id=speler_id)


@app.get("/beker/", response_model=list[schemas.Beker])
def lees_beker(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    beker = crud.get_beker(db, skip=skip, limit=limit)
    return beker


@app.delete("/beker/{beker_id}")
def verwijder_beker(beker_id: int, db: Session = Depends(get_db)):
    crud.verwijder_beker(db=db, beker_id=beker_id)
    return {"message": f"succesvol verwijderd beker met id: {beker_id}"}


