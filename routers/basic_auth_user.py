"""
Autenticación (Auth) vs Autorización

Autenticación => Identificarse -> Usar estándares
Autorización => Tener permisos para hacer operaciones 

Ej: YouTube, cuando inicio sesión, me estoy autenticando, cuando voy a revisar mi panel como creador de contenido, sólo yo lo puedo hacer, porque estoy autorizado.

Ahora vamos a hacer una autenticación básica (Usuario y contraseña)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#OAuth2PasswordBearer => Autenticar el usuario
#OAuth2PasswordRequestForm => La forma en la que los datos deben recibirse y enviarse

router = APIRouter(prefix='/basic', tags=["Basic Auth"], responses={404: {'message': 'No encontrado'}}) # => Creando un prefijo para las rutas
oauth2 = OAuth2PasswordBearer(tokenUrl='login') #Darle la URL que se va a encargar de la autenticación ↓


#Lo de la contraseña no se pone aquí, porque pues no se devuelve, eso va en la DB
class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool # => Este parámetro sería para decir que el usuario ya se fue bien a la mierda


#Heredando el usuario
class UserDB(User): # => Este parámetro sería para decir que el usuario ya se fue bien a la mierda
    password: str


users_db = {
    'CarlMcGar': {
        'username': 'CarlMcGar',
        'name': 'Carlos',
        'email': 'cgarcias',
        'disabled': False,
        'password': '45874' #TODO => Aplicar hash 
    },
    'JerryCaVerg': {
        'username': 'JerryCaVerg',
        'name': 'Jerry',
        'email': 'jeri',
        'disabled': True,
        'password': '123456' #TODO => Aplicar hash 
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales inválidas',
            headers={'WWW-Authenticate': 'Bearer'} # Cabecera corregida
        )
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario deshabilitado')
    return user


#Dejamos el depends solito por ahora para indicar que no depende de nada
@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario incorrecto')
    
    user = search_user_db(form.username)
    if form.password != user.password:  # Comparación corregida
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Contraseña incorrecta')
    
    return {'access_token': user.username, 'token_type': 'bearer'}


@router.get('/users/me')
async def me(user: User = Depends(current_user)): #Esta depende de current_user ↑
    return user