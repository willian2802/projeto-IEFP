# MONGODB_URI = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

uri = "mongodb+srv://williansouza11922:Herika40@cluster0.ajgv5lu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


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


