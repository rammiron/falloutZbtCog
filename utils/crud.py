from utils.db_alchemy import get_db
from .models import User, Whitelist


def get_users_count():
    db = next(get_db())
    return db.query(User).count()


def get_users():
    db = next(get_db())
    return db.query(User).all()


def get_users_from_whitelist():
    db = next(get_db())
    return db.query(Whitelist).all()


def get_users_discord_id():
    db = next(get_db())
    return db.query(User.discord_id).all()


def discord_id_was_found_in_users_db(discord_id: int):
    db = next(get_db())
    was_found = db.query(User).get(discord_id)
    if was_found:
        return True
    else:
        return False


def user_id_was_found_in_whitelist(user_id: int):
    db = next(get_db())
    was_found = db.query(Whitelist).filter(Whitelist.user_id == user_id).first()
    if was_found:
        return True
    else:
        return False


def get_whitelist_users_discord_id():
    db = next(get_db())
    return db.query(Whitelist.user_id).all()


def get_game_id_by_discord_id(discord_id: int):
    db = next(get_db())
    user = db.query(User.user_id).filter(User.discord_id == discord_id).first()
    if user is None:
        return None
    return user[0]


def add_user_to_whitelist(user_id: str):
    db = next(get_db())
    user = Whitelist(user_id=user_id)
    db.add(user)
    db.commit()


def delete_user_from_whitelist(user_id: int):
    db = next(get_db())
    user = db.query(Whitelist).filter(Whitelist.user_id == user_id).first()
    db.delete(user)
    db.commit()
