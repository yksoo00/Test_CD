from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import pytz

Base = declarative_base()
KST = pytz.timezone("Asia/Seoul")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(KST),
        onupdate=lambda: datetime.now(KST),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    prescriptions = relationship("Prescription", back_populates="user")
    chatrooms = relationship("Chatroom", back_populates="user")


class Mentor(Base):
    __tablename__ = "mentor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(KST),
        onupdate=lambda: datetime.now(KST),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    prescriptions = relationship("Prescription", back_populates="mentor")
    chatrooms = relationship("Chatroom", back_populates="mentor")


class Prescription(Base):
    __tablename__ = "prescription"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("mentor.id"), nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(KST),
        onupdate=lambda: datetime.now(KST),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="prescriptions")
    mentor = relationship("Mentor", back_populates="prescriptions")


class Chatroom(Base):
    __tablename__ = "chatroom"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("mentor.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(KST),
        onupdate=lambda: datetime.now(KST),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="chatrooms")
    mentor = relationship("Mentor", back_populates="chatrooms")
    chats = relationship("Chat", back_populates="chatroom")


class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    chatroom_id = Column(Integer, ForeignKey("chatroom.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    is_user = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(KST))
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(KST),
        onupdate=lambda: datetime.now(KST),
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    chatroom = relationship("Chatroom", back_populates="chats")
