from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class LostCategory(str, Enum):
    JEWELRY = "jewelry"
    SILVER = "silver"
    PET = "pet"
    WALLET = "wallet"
    PHONE = "phone"
    KEYS = "keys"
    BAG = "bag"
    DOCUMENTS = "documents"
    VEHICLE = "vehicle"
    OTHER = "other"


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    city: str
    contact: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LostItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    title: str
    description: str
    category: LostCategory
    city: str
    neighborhood: Optional[str] = None
    lost_at: Optional[datetime] = None
    photo_url: Optional[str] = None
    status: str = "lost"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Comment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    item_id: UUID
    user_id: UUID
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Chat(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    item_id: UUID
    members: List[UUID]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    chat_id: UUID
    sender_id: UUID
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
