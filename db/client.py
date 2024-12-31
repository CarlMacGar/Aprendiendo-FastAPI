"""Encargado de gestionar la conexión a la base de datos MongoDB"""

from pymongo import MongoClient

uri = "mongodb+srv://test:test@cursopython.zn0io.mongodb.net/?retryWrites=true&w=majority&appName=CursoPython"

"""Para hacer que el cliente siempre apunte al localhost, se puede hacer de la siguiente manera:"""
#db_client = MongoClient() #Por defecto se conecta a localhost
#db_client = MongoClient().local # => Con esto me ahorro el poner db_client.local.users.find() y pongo db_client.users.find()

"""Para hacer que el cliente apunte a un servidor en específico, se puede hacer de la siguiente manera:"""
db_client = MongoClient(uri).test