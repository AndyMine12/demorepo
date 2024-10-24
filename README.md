# Small web service for Docker practice in "Cloud Computing" #
## Made with FastAPI in Python ##

Copiar contenido del archivo .env.template en un nuevo archivo creado .env en el mismo directorio donde se encuentra el archivo .env.template

### Para levantar el servicio localmente ###
Crear un entorno virtual de python desde la raiz del repositorio
```
python -m venv venv
```

Abrir el venv recién creado
```
venv\Scripts\activate.bat #Para Windows

source venv/bin/activate #Para Linux
```
Descargar las dependencias
```
pip install -r requirements.txt
```
Levantar el servicio con uvicorn
```
uvicorn src.main:app
```

La variable de entorno DB_PORT debe ser igual a 5432 para que el contenedor funcione
Debido a la forma en que se encuentra configurada la instancia de Postgres a utilizar
