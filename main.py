import os

####### PUERTOS #######################

user_service_port = 5000
authentication_service_port = 5001
prediction_service_port = 5002
log_service_port = 5003

#######################################

def main():
    """Menú interactivo"""
    
    print("*** EVALUACION DE RIESGO CARDIACO ***")
    print("\nLos puertos que se van a utilizar son:")
    print("+ user_service: "+str(user_service_port))
    print("+ authentication_service: "+str(authentication_service_port))
    print("+ prediction_service: "+str(prediction_service_port))
    print("+ log_service: "+str(log_service_port))
    print("--- Recuerde que los puertos se pueden cambiar en el archivo "+os.path.basename(__file__)+" --- ")

    while(True):
        print("\nElija una opción y precione enter:")
        option = input("1 - Cargar la Base de Datos MongoDB con los datos\n2 - Levantar los servicios\n3 - Bajar los servicios\n4 - Salir\nrespuesta [1,2,3,4]:")
        print("\n")
        match option:
            case "1": 
                cargar_db()
            case "2":
                levantar_servicios()
            case "3":
                bajar_servicios()
            case "4":
                break
            case _:
                print("debe elegir una opción entre 1 y 4")

def cargar_db():
    """Carga la Base de Datos de MongoDB con los datos"""
  
    import pymongo
    dbClient = pymongo.MongoClient('mongodb://mongoadmin:secret@localhost')
    db = dbClient['riesgo_cardiaco']
    usuarios = [
    {'key': '741f24cf76d772b15dcdd896d6044812', 'tipo': 'freemium'},
    {'key': '7803f9b4f94ab605f48087da2c2a1627', 'tipo': 'premium'},
    {'key': '2ed4bbc82dd29faeb4487092bdc535ed', 'tipo': 'freemium'},
    {'key': '61ca6ffc6b94545a58a75ce0637ebf36', 'tipo': 'premium'},
    {'key': '33d253c53e5739e7024a4f25abc81b22', 'tipo': 'freemium'},
    {'key': 'fb2f370aa9053ca5bb107d888180f94a', 'tipo': 'premium'},
    ]
    db['usuarios'].insert_many(usuarios)

def levantar_servicios():
    """Levanta todos los servicios con los puertos definidos"""

    # Servicio Authentication
    command = "cd microservices; . .venv/bin/activate; flask --app authentication_service.py run --port "+str(authentication_service_port)+" &"
    os.system(command)

    # Servicio Prediction
    command = "cd microservices; . .venv/bin/activate; flask --app prediction_service.py run --port "+str(prediction_service_port)+" &"
    os.system(command)

    # Servicio Log
    command = "cd microservices; . .venv/bin/activate; flask --app log_service.py run --port "+str(log_service_port)+" &"
    os.system(command)

    # Servicio User
    command = "cd microservices; . .venv/bin/activate; flask --app 'user_service:create_app("+str(authentication_service_port)+","+str(prediction_service_port)+","+str(log_service_port)+")' run --port "+str(user_service_port)+" &"
    os.system(command)

def bajar_servicios():
    """Baja todos los servicios"""

    command = "killall flask"
    os.system(command)

main()