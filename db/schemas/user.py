"""Aquí van a estar las operaciones para el modelo de usuario."""

def user_schema(user) -> dict:
    return {
      'id': str(user['_id']),
      'username': user['username'],
      'email': user['email'],
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users] #Se pasa por el esquema cada usuario