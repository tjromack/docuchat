from .database import Base, engine, SessionLocal, get_db
from .document import Document
from .conversation import Conversation, Message

# Create all tables
Base.metadata.create_all(bind=engine)