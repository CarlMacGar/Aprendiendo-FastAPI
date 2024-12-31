## Overview

Se crea una API con FastAPI, siguiendo este curso

[Curso de python desde CERO para backend ~Mouredev](https://www.youtube.com/watch?v=_y9qQZXE24A&t=20488s)

[Repositorio original](https://github.com/mouredev/Hello-Python)

## Entorno virtual (Virtual Env)

~~~ bash
python3 -m venv venv
source venv/bin/activate
~~~

## Dependencias
~~~bash
pip install -r requirements.txt
~~~

## Inicio del servidor
* Local
~~~bash
uvicorn main:app --reload
~~~

##### Notas personales
Para iniciar la base de datos local (Linux)
~~~bash
sudo systemctl start mongod
~~~
* Ya está subida a MongoDB Atlas (Plan Gratuito)
* Buscando para desplegar ya que DETA está desconectado 😔