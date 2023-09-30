from typing import Any


class User:
    timestamp: int
    chat_id: str
    name: str
    username: str
    credit: int

    def __init__(
        self, timestamp: int, chat_id: str, name: str, username: str, credit: int
    ) -> None:
        self.timestamp = timestamp
        self.chat_id = chat_id
        self.name = name
        self.username = username
        self.credit = credit

    @staticmethod
    def from_dict(obj: Any) -> "User":
        assert isinstance(obj, dict)
        timestamp = obj.get("timestamp")
        chat_id = obj.get("chat_id")
        name = obj.get("name")
        username = obj.get("username")
        credit = obj.get("credit")
        return User(timestamp, chat_id, name, username, credit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["timestamp"] = self.timestamp
        result["chat_id"] = self.chat_id
        result["name"] = self.name
        result["username"] = self.username
        result["credit"] = self.credit
        return result
