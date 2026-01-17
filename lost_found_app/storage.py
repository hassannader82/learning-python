from __future__ import annotations

from collections import defaultdict
from typing import Dict, List
from uuid import UUID

from .models import Chat, Comment, LostItem, Message, User


class InMemoryStore:
    def __init__(self) -> None:
        self.users: Dict[UUID, User] = {}
        self.items: Dict[UUID, LostItem] = {}
        self.comments: Dict[UUID, Comment] = {}
        self.chats: Dict[UUID, Chat] = {}
        self.messages: Dict[UUID, Message] = {}
        self.item_comments: Dict[UUID, List[UUID]] = defaultdict(list)
        self.chat_messages: Dict[UUID, List[UUID]] = defaultdict(list)

    def add_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def add_item(self, item: LostItem) -> LostItem:
        self.items[item.id] = item
        return item

    def add_comment(self, comment: Comment) -> Comment:
        self.comments[comment.id] = comment
        self.item_comments[comment.item_id].append(comment.id)
        return comment

    def add_chat(self, chat: Chat) -> Chat:
        self.chats[chat.id] = chat
        return chat

    def add_message(self, message: Message) -> Message:
        self.messages[message.id] = message
        self.chat_messages[message.chat_id].append(message.id)
        return message

    def get_comments_for_item(self, item_id: UUID) -> List[Comment]:
        return [self.comments[cid] for cid in self.item_comments[item_id]]

    def get_messages_for_chat(self, chat_id: UUID) -> List[Message]:
        return [self.messages[mid] for mid in self.chat_messages[chat_id]]
