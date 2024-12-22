from fastapi import APIRouter

#Como esto es otro módulo de la API principal, se hace con APIRouter


router = APIRouter(prefix='/products', #Operación prefix para no andar poniendo a cada rato la ruta, sino en caso de parámetros y agregaciones
                   tags=['products'], #Para separar en la documentación
                   responses={404: {'message': 'No encontrado'}}) #En caso de que no funcione

products_list = ['Quipito', 'Zungas', 'Polvora']

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]