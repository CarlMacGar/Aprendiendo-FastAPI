from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/users', tags=['users'], responses={404:{'message': 'No encontrado'}})

#Entidad usuario
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

test_users = [User(name='Kirby', surname='Hernandez', url='Kirby', age=100, id=1),User(name='Dr', surname='Mario', url='Smash Bros', age=30, id=2)]

#Inicio del server: uvicorn users:app --reload

@router.get("/json", summary="Ruta de usarios estáticos", description="")
async def users_json():
    return [{'name': 'Carl', 'surname': 'Gar', 'url':'Aún no', 'age': 12},{'name': 'Lejo', 'surname': 'Gom', 'url':'Si', 'age': 8}]

@router.get("/class", summary="Ruta de usarios estáticos creado con Basemodel", description="")
async def users_test():
    return User(name='Carl', surname='Gerardo', url='no', age=15, id=3)

@router.get("/", summary="Ruta de la lista de usuarios", description="")
async def users_test():
    return test_users

"""CRUD"""
def search_user(id: int):
    users = filter(lambda user: user.id==id , test_users)
    try:
        return list(users)[0]
    except:
        return {'error': 'User not found'}

#Llamada en el path
@router.get('/{id}')
async def user(id: int):
    return search_user(id)

#Llamada en query => Se hace ponientolo así: [ruta]/userquery/?id=[id] //Si se quiere concatenar ?id=[id]&name=[name] 
@router.get('/query')
async def user(id:int):
    return search_user(id)

#Para cambiarle el código de respuesta se hace aquí en el @app.post para el caso ideal, sino se importa HTTPException    
@router.post('/create', response_model=User, status_code=201)
async def create_user(user: User): 
    try:
        if(type(search_user(user.id)) == User):
            raise HTTPException(404, detail='El usuario ya existe') #Para lanzar la excepción se hace con raise
        test_users.append(user)
        return user
    except:
        raise HTTPException(500,detail='No se ha podido crear el usuario')

@router.put('/update')
async def update_user(user: User):
    updated = False
    for index, saved_user in enumerate(test_users):
        if saved_user.id == user.id:
            test_users[index] = user
            updated = True
    return {'error': 'No se ha actualizado el usuario'} if not updated else user, updated

@router.delete('/{id}')
async def delete_user(id: int):
    deleted = False
    try:
        for index, saved_user in enumerate(test_users):
            if saved_user.id == id:
                del test_users[index]
                deleted = True
        return {'error': 'No se ha eliminado el usuario'} if not deleted else deleted
    except:
        return 'No se ha podido eliminar el usuario :P'