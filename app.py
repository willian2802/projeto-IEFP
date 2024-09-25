from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from logs import log_register
from DB import register_user, login_user_part2, login_user_part1, grab_secret_question, get_logs_from_db
import pyotp
import secrets
from functools import wraps


from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)


# jwt = JWTManager(app, secret_key='sua_chave_secreta')

# # Crie uma função para gerar o token de acesso: 
# def generate_token(user_id): 
#     return create_access_token(identity=user_id)

# # Crie uma função para proteger as rotas que precisam de autenticação
# @jwt_required 
# def protected_route(): 
#     return 'Olá, usuário autenticado!'

app.secret_key = secrets.token_urlsafe(16)

# # Use o token de acesso para autenticar o usuário em cada requisição
# access_token = generate_token(user_id)


# app.secret_key = 'supersecret_key' # Necessário para usar sessões


#  Pagina inicial
@app.route('/', methods=['GET', 'POST'])
def render_login():
    log_register()
    return render_template('login.html')

@app.route('/Secure_Login', methods=['POST'])
def login():

    # Capturar os dados enviados no corpo da requisição
    login_data = request.get_json()

    login_part = login_data['login_process']

    #  part1 do login e apens o nome e a senha
    #  part2 do login e a pergunta de segurança e a resposta
    if login_part == "part1":
        login_part1_resposta = login_user_part1(login_data)
        session['username'] = login_data['Name']

        if login_part1_resposta == False:
            return jsonify({"status": "Login incorreto. Tente novamente."})

        #  Retorna a pergunta de segurança para o javaScript para ser renderizado na pagina
        pergunta_seguranca = grab_secret_question(session['username'])

        return jsonify({"status": pergunta_seguranca})
    else:
        login_data['Name'] = session['username']
        login_part2_resposta = login_user_part2(login_data, session['username'])

    if login_part2_resposta == True:
        session['authenticated'] = True
        return jsonify({'success': True, 'message': 'Login successful'})
    
    return jsonify({"status": " tentativa de Login mal-sucedida."})
    

@app.route('/Register_New_Account', methods=['POST'])
def Create_Account():
    # Capturar os dados enviados no corpo da requisição
    New_account_data = request.get_json()

    resposta_do_DB = register_user(New_account_data)

    # retornar True sequeinifica que o nome de usuario ja existe no DB
    if resposta_do_DB == True:
        return jsonify({"status": "alerta", "message": "Nome de Usuário ja existe. Tente novamente."})

    return resposta_do_DB


@app.route('/logout')
def logout():
    log_register()
    session.pop('authenticated', None)
    return redirect(url_for('render_login'))

def authenticated_required(f):
    @wraps(f)



    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session or not session['authenticated']:
            return 'Você não está autenticado', 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/welcome')
@authenticated_required
def welcome():
    log_register()
    return render_template('welcome.html')


@app.route('/nothing_here', methods=['GET'])
def just_logs():
    Logs_Storage = get_logs_from_db()
    return jsonify(Logs_Storage)


@app.route('/console_logs', methods=['GET'])
def console_logs():
    return render_template('console.html')


if __name__ == '__main__':
    app.run(debug=True)

