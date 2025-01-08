from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from the .env file located in the frontend directory
load_dotenv(dotenv_path='G:/health_fitness_tracker/frontend/.env')

Base = declarative_base()

# Define models (User, Workout, Exercise, Nutrition, HealthMetric) as you have done

# Database connection using environment variables
DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

# Create tables with error handling
try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error creating tables: {e}")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    health_metrics = relationship("HealthMetric", back_populates="user", cascade="all, delete-orphan")
    nutrition = relationship("Nutrition", back_populates="user", cascade="all, delete-orphan")

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id', ondelete="CASCADE"))
    name = Column(String, nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    workout = relationship("Workout", back_populates="exercises")

class Nutrition(Base):
    __tablename__ = 'nutrition'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    date = Column(DateTime, default=datetime.utcnow)
    meal = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    user = relationship("User", back_populates="nutrition")

class HealthMetric(Base):
    __tablename__ = 'health_metrics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float)
    heart_rate = Column(Float)
    user = relationship("User", back_populates="health_metrics")

# Database connection
# engine = create_engine(DB_URL)

# Create tables
Base.metadata.create_all(engine)
