from pydantic import BaseModel
from datetime import datetime

class Note(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    create_at: datetime
    updated_at: datetime

class SharedNote(BaseModel):
    id: int
    note_id: int
    user_id: int
    permission_level: int

class NoteLink(BaseModel):
    id: int
    source_note_id: int
    target_note_title: str