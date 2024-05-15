from sqlalchemy.orm import Session

import models
import schemas
import auth


def get_player(db: Session, speler_id: int):
    return db.query(models.Speler).filter(models.Speler.id == speler_id).first()


def get_player_by_email(db: Session, email: str):
    return db.query(models.Speler).filter(models.Speler.email == email).first()


def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Speler).offset(skip).limit(limit).all()


def create_player(db: Session, speler: schemas.PlayerCreate):
    hashed_password = auth.get_password_hash(speler.hashed_password)
    db_speler = models.Speler(naam=speler.naam, achternaam=speler.achternaam, email=speler.email, hashed_password=hashed_password,leeftijd=speler.leeftijd, nationaliteit=speler.nationaliteit)
    db.add(db_speler)
    db.commit()
    db.refresh(db_speler)
    return db_speler

def update_player(db: Session, speler: schemas.PlayerCreate, speler_id: int):
    db_speler = get_player(db=db, speler_id=speler_id)
    db_speler.naam = speler.naam
    db_speler.achternaam = speler.achternaam
    db_speler.email= speler.email
    db_speler.hashed_password= speler.hashed_password
    db_speler.leeftijd = speler.leeftijd
    db_speler.nationaliteit = speler.nationaliteit
    db_speler.club = speler.club
    db.commit()
    db.refresh(db_speler)
    return db_speler


def delete_player(db: Session,speler_id: int):
    db.query(models.Speler).filter(models.Speler.id== speler_id).delete()
    db.commit()

def get_competitie(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Compititie).offset(skip).limit(limit).all()


def maak_speler_compititie(db: Session, compititie: schemas.CompititieCreate, speler_id: int):
    db_compititie = models.Compititie(**compititie.dict(), compititie_id=speler_id)
    db.add(db_compititie)
    db.commit()
    db.refresh(db_compititie)
    return db_compititie


def verwijder_compititie(db: Session,compititie_id: int):
    db.query(models.Compititie).filter(models.Compititie.id== compititie_id).delete()
    db.commit()

def get_beker(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Beker).offset(skip).limit(limit).all()


def maak_speler_beker(db: Session, beker: schemas.BekerCreate, speler_id: int):
    db_beker = models.Beker(**beker.dict(), beker_id=speler_id)
    db.add(db_beker)
    db.commit()
    db.refresh(db_beker)
    return db_beker


def verwijder_beker(db: Session,beker_id: int):
    db.query(models.Beker).filter(models.Beker.id== beker_id).delete()
    db.commit()

def create_user(db: Session, speler: schemas.PlayerCreate):
    hashed_password = auth.get_password_hash(speler.hashed_password)
    db_user = models.Speler(email=speler.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user