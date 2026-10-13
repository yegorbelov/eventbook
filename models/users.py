from typing import List, Optional

from models import User


def add_user(users: List[User], name: str) -> User:
    user_id = len(users) + 1
    user = User(user_id, name)
    users.append(user)
    return user


def find_user_by_name(users: List[User], name: str) -> Optional[User]:
    for user in users:
        if user.name == name:
            return user
    return None


def find_or_create_user(users: List[User], name: str) -> User:
    user = find_user_by_name(users, name)
    if user is not None:
        return user
    return add_user(users, name)
