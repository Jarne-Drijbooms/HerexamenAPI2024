from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Speler(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    naam = Column(String, index=True)
    achternaam = Column(String, index=True)
    leeftijd = Column(Integer, index=True)
    email = Column(String, unique=True, index=True)
    nationaliteit = Column(String, index=True)
    team = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    compititie = relationship("Compititie", back_populates="compititie")
    beker = relationship("Beker", back_populates="beker")


class Compititie(Base):
    __tablename__ = "compititie"

    id = Column(Integer, primary_key=True, index=True)
    hoogste_positie = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    compititie_id = Column(Integer, ForeignKey("spelers.id"))

    compietitie = relationship("player", back_populates="compititie")

class Beker(Base):
    __tablename__ = "beker"

    id = Column(Integer, primary_key=True, index=True)
    hoogste_positie = Column(Integer, index=True)
    huidige_positie = Column(Integer, index=True)
    beker_id = Column(Integer, ForeignKey("spelers.id"))

    beker = relationship("player", back_populates="beker")