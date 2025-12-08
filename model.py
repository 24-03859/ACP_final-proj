import random
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

base_path = os.path.dirname(__file__)

data_dir = os.path.join(base_path, "DATA_ADMIN_ONLY_OY!!!")
os.makedirs(data_dir, exist_ok=True)
users_db_path = os.path.join(data_dir, "datasetsko.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)

engine = create_engine(f"sqlite:///{users_db_path}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(engine)

def load_saved_users():
    session = SessionLocal()
    try:
        rows = session.query(User).order_by(User.id).all()
        return [row.username for row in rows]
    except Exception as exc:
        messagebox.showwarning("Database Error", f"Unable to load users:\n{exc}")
        return []
    finally:
        session.close()

def add_user_to_db(username):
    session = SessionLocal()
    try:
        if session.query(User).filter_by(username=username).first():
            return False
        session.add(User(username=username))
        session.commit()
        return True
    except Exception as exc:
        session.rollback()
        messagebox.showwarning("Database Error", f"Unable to save user:\n{exc}")
        return False
    finally:
        session.close()

def delete_user_from_db(username):
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False
        session.delete(user)
        session.commit()
        return True
    except Exception as exc:
        session.rollback()
        messagebox.showwarning("Database Error", f"Unable to delete user:\n{exc}")
        return False
    finally:
        session.close()

def reload_users():
    global saved_users
    saved_users = load_saved_users()