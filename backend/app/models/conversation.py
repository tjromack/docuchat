from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), default="New Chat")
    created_date = Column(DateTime, server_default=func.now())
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    message_type = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    source_documents = Column(Text)  # JSON string of source document references
    
    # Relationship back to conversation
    conversation = relationship("Conversation", back_populates="messages")