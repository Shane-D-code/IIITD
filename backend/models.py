from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    token_hash = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScanResult(Base):
    __tablename__ = "scan_results"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    url_hashes = Column(JSON)
    risk_score = Column(Float)
    high_risk_link_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()