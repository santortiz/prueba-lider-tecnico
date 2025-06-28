from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 👇 Esto creará las tablas automáticamente al importar database.py desde main.py
def create_tables_if_not_exist():
    import app.models  # Asegúrate de importar todos los modelos para que estén registrados
    Base.metadata.create_all(bind=engine)
