from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column,Integer,String, DateTime, Float
import sqlalchemy.exc

engine = create_engine(
    'sqlite:///Finder.db',
    pool_size=10,  # Taille du pool de connexions
    max_overflow=20,  # Nombre de débordements autorisés
    pool_timeout=30,  # Temps d'attente avant de lever une exception
    pool_recycle=3600,  # Taille du pool de connexions
    )

# Création de la session et du modèle de base
Session = sessionmaker(bind=engine)

Base = declarative_base()