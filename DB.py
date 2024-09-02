
from flask import session

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import datetime

uri = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['sample_mflix']
IEFP_users_collection = db['IEFP_Users']

def connect_to_mongo():
    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return "You successfully connected to MongoDB!"
    except Exception as e:
        print(e)
        return "Failed to connect to MongoDB"

def add_log_to_DB(log):

    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Selecionar uma coleção
    colecao = db['IEFP_Logs']

    # insere o log no DB
    colecao.insert_one(log)


def add_IP_data_to_DB(ip_address, data):
    db = client['sample_mflix']
    colecao = db['IEFP_IP_Data']

    update = {"$set": data}  # Update the existing document with the new data
    filter = {"_id": ip_address}  # Filter the document by _id

    # atualiza o IP_data no DB
    result = colecao.update_one(filter, update)

    # se nada for encontrado, insere um novo IP_data no DB
    if result.matched_count == 0:
        document = {"_id": ip_address, **data}
        colecao.insert_one(document)
        print(f"Document inserted with ID: {ip_address}")

# ----------- IP DATA DB -----------

def add_IP_data_to_DB(new_ip_data):

    # Selecionar o banco de dados
    db = client['sample_mflix']

    # Selecionar uma coleção
    colecao = db['IP_Data']

    # insere o log no DB
    colecao.insert_one(new_ip_data)
    
    print (f"Document inserted with ID: {new_ip_data}")



def get_ip_data_from_db(ip_address):
    
    db = client['sample_mflix']
    colecao = db['IP_Data']

    # Encontrar o documento que contém o IP especificado como uma chave no documento
    data = colecao.find_one({ip_address: {"$exists": True}})
    
    print(data)
    # Se encontrado, retorna os dados do IP específico
    if data and ip_address in data:
        return data[ip_address]
    return None




#  ------------- Login e registro de usuário ----------------

def register_user(Register_data):

    username = Register_data['Name']
    password = Register_data['Password']
    Pergunta_secreta = Register_data['Pergunta_Seguranca']
    Resposta = Register_data['resposta_Secreta']
    Nivel_acesso = 1

    IEFP_users_collection.insert_one({
        'Nome': username,
        'Nivel_acesso': Nivel_acesso,
        'Senha': password,
        "Pergunta_secreta": Pergunta_secreta,
        "resposta_Secreta": Resposta,
        "created_at": datetime.datetime.now()
    })

    return "Usuário registrado com sucesso"


from flask import g

def login_user_part1(login_data):
    username = login_data['Name']
    password = login_data['Password']

    # Lógica de login
    user = IEFP_users_collection.find_one({"Nome": username, "Senha": password})

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(user)

    if user:
        g.user_id = str(user['_id'])
        return True
    else:
        return False
    
def login_user_part2(login_data, username):

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(login_data)

    username = login_data['Name']
    resposta_secreta = login_data['resposta_Secreta']

    user = IEFP_users_collection.find_one({"Nome": username, "Senha": resposta_secreta})

    print(user)

    if user:
        g.user_id = str(user['_id'])
        return True
    else:
        return False



