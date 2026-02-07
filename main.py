from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://admin:admin@localhost:5432/testdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(UserCreate):
    id: int

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.name = user.name
    db_user.age = user.age
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user
