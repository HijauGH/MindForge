from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Enum, text
from typing import Annotated, List
from datetime import datetime
import enum as e
from Secure import get_password_hash, verify_password
from database import *


int_pk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):     #Таблица с пользователями
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    #Создадим отношения между таблицами(связь: один-ко-многим)
    notes: Mapped[List["Note"]] = relationship(back_populates="user")
    shared_note: Mapped[List["SharedNote"]] = relationship(back_populates="user")

    #Хэшируем пароли
    def set_password(self, password: str):
        self.hashed_password = get_password_hash(password)


    def check_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(150))
    content: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )

    #Создаем отношения(связь: многие-к-одному)
    user: Mapped["User"] = relationship(back_populates="notes")
    shared_note: Mapped[list["SharedNote"]] = relationship(back_populates="note")


class PermissionLevel(e.Enum):
    VIEW = "view"
    EDIT = "edit"


class SharedNote(Base):
    __tablename__ = "shared_notes"

    id: Mapped[int_pk]
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    permission_level: Mapped[PermissionLevel] = (
        mapped_column(
            Enum(PermissionLevel, values_callable=lambda x: [e.value for e in x]),
            default=PermissionLevel.VIEW
        )
    )

    note: Mapped["Note"] = relationship(back_populates="shared_note")
    user: Mapped["User"] = relationship(back_populates="shared_note")


class NoteLink(Base):
    __tablename__ = "note_link"

    id: Mapped[int_pk]
    source_note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    target_note_name: Mapped[str] = mapped_column(String(150))

    source_note: Mapped["Note"] = relationship(back_populates="outgoing_links")


