"""Aquí vamos a ver cómo hacer una autenticación con JWT (Json Web Token), es decir un token encriptado que se va a encargar de la autenticación del usuario"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta # => Para la duración del token, timedelta es para hacer calculos con fechas


ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION_MIN = 1
SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # => Aquí va la clave secreta para encriptar el token, algo para hacerlo más seguro, ya que solo nosotros sabremos cual es => Con openssl rand -hex 32 se puede generar una clave secreta

router = APIRouter(prefix='/jwt', tags=["JWT Auth"], responses={404: {'message': 'No encontrado'}}) # => Creando un prefijo para las rutas

#Hay que definir nuestro contexto de encriptación con passlib.context y el esquema que vamos a usar
crypt = CryptContext(schemes=['bcrypt'])


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
        'password': '$2a$12$XAdS7nPy29uMinxNyPoWfu8NtJ/biMgo86FCCHE64SSDZ5yk5NxGe'
    },
    'JerryCaVerg': {
        'username': 'JerryCaVerg',
        'name': 'Jerry',
        'email': 'jeri',
        'disabled': True,
        'password': '$2a$12$FzLpS6tMVWkJbWSRn4BQ9uNCY0Yg79Q0GB9XaZwyz9yz2UkjVwqh.' 
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


#Dependencia para obtener el token
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales inválidas', headers={'WWW-Authenticate': 'Bearer'})

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    user = search_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario no encontrado')
    
    return user


async def current_user(user: User = Depends(auth_user)):
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
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Contraseña incorrecta')

    #Creando el token
    expired = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION_MIN)
    acces_token = jwt.encode({'sub': user.username, 'exp': expired},SECRET, ALGORITHM)


    return {'access_token': acces_token, 'token_type': 'bearer'}


@router.get('/users/me')
async def me(user: User = Depends(current_user)): #Esta depende de current_user ↑
    return user