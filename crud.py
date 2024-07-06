import sqlalchemy
from db_alchemy import get_db
from utils.models import User, Whitelist


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


def discord_id_was_found_in_whitelist(discord_id: int):
    db = next(get_db())
    was_found = db.query(Whitelist).get(discord_id)
    if was_found:
        return True
    else:
        return False


def get_whitelist_users_discord_id():
    db = next(get_db())
    return db.query(Whitelist.discord_id).all()


def get_game_id_by_discord_id(discord_id: int):
    db = next(get_db())
    return db.query(User.user_id).filter(User.discord_id == discord_id).first()[0]


def add_user_to_whitelist(discord_id: int, user_id: str):
    db = next(get_db())
    user = Whitelist(user_id=user_id, discord_id=discord_id)
    db.add(user)
    db.commit()
