import pymongo
from datetime import datetime, timedelta
from flask import (
    Flask,
    request,
    abort,
    g
)  # se importa la librería principal de flask

def create_app(db_connection_string,test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    @app.route('/authentication_service',methods = ['POST'])
    def authentication_service():
        """Microservicio que autoriza al usuario"""

        key = request.headers.get('Authorization')

        if not key:
            abort(400, "Falta el header Authorization con la API key")
        
        # Validación de usuario autorizado
        tipo = usuario_registrado(db_connection_string,key)
        if not tipo:
            abort(403, "El usuario no esta registrado")
        
        # Validación de la cantidad de solicitudes por minuto
        if alcanzo_maximo(db_connection_string,key,tipo):
            abort(429, "El usuario alcanzo el maximo de solicitudes por minuto")

        return ["El usuario está autorizado"]
    return app

def get_db(db_connection_string:str):
    """Se establece la conexión a la base de datos"""
    
    if 'db' not in g:
        dbClient = pymongo.MongoClient(db_connection_string)
        db = dbClient['riesgo_cardiaco']
        g.db= db
    return g.db

def usuario_registrado(db_connection_string:str,hash:str):
    """Contrasta la key ingresada contra la BD"""
    
    result = get_db(db_connection_string)['usuarios'].find_one({'key': hash})
    if result:
        return result["tipo"]
    else:
        return False
    
def alcanzo_maximo(db_connection_string:str, key:str, tipo:str):
    "Verifica que el usuario no exceda la cantidad máxima de solicitudes por minuto"
    
    if tipo == "freemium":
        maximo = 5
    else:
        maximo = 50
    
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    query = {"$and":[{"key": key},{"fecha": {"$gte": str(one_minute_ago)}}]}
    solicitudes = get_db(db_connection_string)['bitacora'].count_documents(query)    
    if solicitudes >= maximo:
        return True
    return False
