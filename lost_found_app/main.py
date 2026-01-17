from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException

from .models import Chat, Comment, LostCategory, LostItem, Message, User
from .storage import InMemoryStore

app = FastAPI(title="Lost & Found API", version="0.1.0")
store = InMemoryStore()


@app.post("/users", response_model=User)
def create_user(name: str, city: str, contact: str) -> User:
    user = User(name=name, city=city, contact=contact)
    return store.add_user(user)


@app.post("/items", response_model=LostItem)
def create_item(
    user_id: UUID,
    title: str,
    description: str,
    category: LostCategory,
    city: str,
    neighborhood: Optional[str] = None,
    lost_at: Optional[datetime] = None,
    photo_url: Optional[str] = None,
) -> LostItem:
    if user_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")
    item = LostItem(
        user_id=user_id,
        title=title,
        description=description,
        category=category,
        city=city,
        neighborhood=neighborhood,
        lost_at=lost_at,
        photo_url=photo_url,
    )
    return store.add_item(item)


@app.get("/items", response_model=List[LostItem])
def list_items(
    city: Optional[str] = None,
    category: Optional[LostCategory] = None,
) -> List[LostItem]:
    items = list(store.items.values())
    if city:
        items = [item for item in items if item.city == city]
    if category:
        items = [item for item in items if item.category == category]
    return items


@app.post("/items/{item_id}/comments", response_model=Comment)
def add_comment(item_id: UUID, user_id: UUID, text: str) -> Comment:
    if item_id not in store.items:
        raise HTTPException(status_code=404, detail="Item not found")
    if user_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")
    comment = Comment(item_id=item_id, user_id=user_id, text=text)
    return store.add_comment(comment)


@app.get("/items/{item_id}/comments", response_model=List[Comment])
def list_comments(item_id: UUID) -> List[Comment]:
    if item_id not in store.items:
        raise HTTPException(status_code=404, detail="Item not found")
    return store.get_comments_for_item(item_id)


@app.post("/items/{item_id}/found", response_model=Chat)
def mark_found(item_id: UUID, finder_id: UUID) -> Chat:
    if item_id not in store.items:
        raise HTTPException(status_code=404, detail="Item not found")
    if finder_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")
    item = store.items[item_id]
    item.status = "found"
    chat = Chat(item_id=item_id, members=[item.user_id, finder_id])
    return store.add_chat(chat)


@app.post("/chats/{chat_id}/messages", response_model=Message)
def send_message(chat_id: UUID, sender_id: UUID, content: str) -> Message:
    if chat_id not in store.chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    if sender_id not in store.users:
        raise HTTPException(status_code=404, detail="User not found")
    if sender_id not in store.chats[chat_id].members:
        raise HTTPException(status_code=403, detail="User not in chat")
    message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    return store.add_message(message)


@app.get("/chats/{chat_id}/messages", response_model=List[Message])
def list_messages(chat_id: UUID) -> List[Message]:
    if chat_id not in store.chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    return store.get_messages_for_chat(chat_id)
