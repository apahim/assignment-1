from sqlalchemy.exc import IntegrityError

from cloudy.model import DB
from cloudy.model import User


def get_all_users():
    users = []
    for user in DB.session.query(User).all():
        users.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,

            }
        )
    return users


def add_user(username, email):
    user = User(username=username, email=email)
    DB.session.add(user)

    try:
        DB.session.commit()
        return {
            'message': f'user [{username}] added successfully'
        }
    except IntegrityError:
        return {
            'message': f'username or email already taken'
        }
