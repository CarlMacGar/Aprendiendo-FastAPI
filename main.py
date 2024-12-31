from fastapi import FastAPI as FAPI

#Importando los ficheros
from routers import products, users, basic_auth_user, jwt_auth_user, users_mongo

#Importar la imágen
from fastapi.staticfiles import StaticFiles #Con esto traemos los archivos estáticos

app = FAPI()

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_user.router)
app.include_router(jwt_auth_user.router)
app.include_router(users_mongo.router)
#Aquí el valor que importa es el de directory como parámetro de StaticFiles, pues ese si es para el recurso.
app.mount('/static', StaticFiles(directory='static'), name='static') #Esto es para la imágen o cualquier otra cosa (Montar) 

#Inicio del server: uvicorn main:app --reload

"""Ver la documentación"""
#Swagger: [ruta]/docs
#Redocly: [ruta]/redoc

@app.get(
    "/", #Ruta
    #Documentación
    summary="Ruta principal", 
    description="Esta ruta retorna un saludo inicial para quienes están aprendiendo FastAPI."
)
async def root():
    return "¡Hola hola, voy a aprender FastAPI :D!"

@app.get(
    "/si", #Ruta
    #Documentación
    summary="Ruta de confirmación",
    description="Retorna un mensaje de confirmación en formato JSON."
)
async def si():
    return {"message": "Si"}

"""
Ahora para lo de la base de datos, vamos a usar mongo
Para instalarlo: pip install pymongo
"""

