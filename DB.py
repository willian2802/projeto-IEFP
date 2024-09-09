
from flask import g

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime

# from dotenv import dotenv_values

# env_vars = dotenv_values('.env')
# uri = env_vars['MONGO_URI']

# Agora, ao invés de usar a string de conexão diretamente no seu código, você pode acessá-la através da variável uri.

# Lembre-se de adicionar o arquivo (.env) ao seu arquivo (.gitignore) para evitar que ele seja commitado no repositório.

# MONGO_URI=<seu_uri_criptografado>


uri = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['sample_mflix']
IEFP_users_collection = db['IEFP_Users']

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

#  ------------- pega a pergunta de segurança do usuario do DB ----------------

def grab_secret_question(username):
    user = IEFP_users_collection.find_one({"Nome": username})
    
    pergunta_secreta = user["Pergunta_secreta"]

    return pergunta_secreta




#  ------------- Login e registro de usuário ----------------

def register_user(Register_data):
    username = Register_data['Name']
    password = Register_data['Password']
    Pergunta_secreta = Register_data['Pergunta_Seguranca']
    Resposta = Register_data['resposta_Secreta']
    Nivel_acesso = 1

    # verifica se o nome de usuário ja esta sendo usado no DB
    existing_user = IEFP_users_collection.find_one({"Nome": username})
    if existing_user:
        return True

    # If no user with the same name exists, insert the new user
    IEFP_users_collection.insert_one({
        'Nome': username,
        'Nivel_acesso': Nivel_acesso,
        'Senha': password,
        "Pergunta_secreta": Pergunta_secreta,
        "resposta_Secreta": Resposta,
        "created_at": datetime.datetime.now()
    })

    return "Usuário registrado com sucesso"

def login_user_part1(login_data):
    username = login_data['Name']
    password = login_data['Password']

    # Lógica de login
    user = IEFP_users_collection.find_one({"Nome": username, "Senha": password})

    if user:
        g.user_id = str(user['_id'])
        return True
    else:
        return False
    
def login_user_part2(login_data, username):

    username = login_data['Name']
    resposta_secreta = login_data['resposta_Secreta']

    user = IEFP_users_collection.find_one({"Nome": username, "resposta_Secreta": resposta_secreta})

    if user:
        g.user_id = str(user['_id'])
        return True
    else:
        return False



