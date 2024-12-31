"""CRUD de usuarios CON base de datos MongoDB""" 
from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson.objectid import ObjectId #Para poder hacer la búsqueda por _id

router = APIRouter(prefix='/userdb',
                   tags=['users on MongoDB'], 
                   responses={status.HTTP_404_NOT_FOUND:{'message': 'No encontrado'}})

#Ahora la entidad usuario se va como modelo a user.py 
test_users = []

#676e5ea487e8e0ead7739bba

"""Utilidades"""
def search_user(field: str, key: any):
    try:
        user = db_client.users.find_one({field: key}) #Lo busca por el email
        return User(**user_schema(user)) #Se retorna el usuario, primero se pasa por el esquema y luego por el modelo
        """
        Diferencia entre User(**user_schema(user)) y User(user_schema(**user))
        User(**user_schema(user)) => Se pasa el diccionario a un modelo
            Es decir -> user_schema(user) retorna { "id": "123", "username": "Hola", "email": "hola@si" }
            Y User(**user_schema(user)) retorna User(id="123", username="Hola", email="hola@si")
        User(user_schema(**user)) => Se pasa el modelo a un diccionario
            Es decir -> si user es { "id": "123", "username": "Hola", "email": "hola@si" }
            con los ** se pasa a user_schema(id="123", username="Hola", email="hola@si")
        """
    except:
        return {'error': 'User not found'}

"""CRUD"""

@router.post('/create', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if type(search_user('email', user.email)) == User:
        raise HTTPException(status.HTTP_409_CONFLICT, detail='El usuario ya existe') 
    try:
        user_dict = dict(user) 
        del user_dict['id']
        
        id = db_client.users.insert_one(user_dict).inserted_id #Se pone 'local.[modelo]' porque es el nombre de la base de datos y el esquema
        
        new_user = user_schema(db_client.users.find_one({'_id': id})) #Se busca el usuario por el _id (que es el id que se le asigna automáticamente)
        return User(**new_user)
    except:
       raise HTTPException(500,detail='No se ha podido crear el usuario')


@router.get("/", response_model=list[User], summary="Ruta de la lista de usuarios", description="")
async def users():
    return users_schema(db_client.users.find())


#Llamada en el path
@router.get('/{id}')
async def user(id: str):
    return search_user('_id', ObjectId(id))


#Llamada en query => Se hace ponientolo así: [ruta]/userquery/?id=[id] //Si se quiere concatenar ?id=[id]&name=[name] 
@router.get('/query/') #Importante poner la barra al final
async def user(id: str):
    return search_user('_id', ObjectId(id))


@router.put('/update', status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict['id']
    try:
        db_client.users.find_one_and_replace({'_id': ObjectId(user.id)}, user_dict)
        return search_user('_id', ObjectId(user.id))
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No se ha actualizad el usuario')


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    try:
        db_client.users.find_one_and_delete({'_id': ObjectId(id)})
    except: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='No se ha encontrado el usuario')