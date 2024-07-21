#  ----------------------------------- tudo que envolve criaçao e manuiulacao de Logs -----------------------------------


from datetime import datetime
from flask import request


Logs_Storage = []

class Log:
    def __init__(self, current_time, ip_address, path, agent,coment):
        self.current_time = current_time
        self.ip_address = ip_address
        self.path = path
        self.agent = agent
        self.coment = coment

    def create_log(self):

        # generate a log
        log = {
        'current_time': self.current_time,
        'IP': self.ip_address,
        'agent': self.agent,
        'path': self.path,
        'coment': self.coment
        }
        Logs_Storage.append(log)

    def show_log(self):
        return f"Current Time: {self.current_time}, IP: {self.ip_address}, Path: {self.path}, Agent: {self.agent}, Hash Code: {self.fingerprint}, Coment: {self.coment}"
    
    def show_all(self):
        return (Logs_Storage)


def log_register():

    # pega as informações
    ip_address = request.remote_addr
    current_time = datetime.now()
    path = request.path
    agent = request.user_agent.string
    coment = request.form.get('coment')

    # cria o log e armazena no Logs_storage
    New_log = Log(current_time, ip_address, path, agent,coment)
    New_log.create_log()
