from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from forms import LoginForm, TwoFactorForm
from logs import log_register
from DB import login_user, register_user, login_user_part2
import pyotp

app = Flask(__name__)


app.secret_key = 'supersecret_key' # Necessário para usar sessões

# Usuário e senha de exemplo
USER_DATA = {
    "username": "testuser",
    "password": "password123",
    "2fa_secret": pyotp.random_base32()
}

#  Pagina inicial
@app.route('/', methods=['GET', 'POST'])
def render_login():
    return render_template('login.html')

@app.route('/Secure_Login', methods=['POST'])
def login():
    # Capturar os dados enviados no corpo da requisição
    login_data = request.get_json()
    print("??????????????????????????????????????????????????????????????????????????????????????????????????????????????")
    print(login_data)

    login_part = login_data['login_part']

    #  part1 do login e apens o nome e a senha
    #  part2 do login e a pergunta de segurança e a resposta
    if login_part == "part1":
        resposta_do_DB = login_user_part1(login_data)
        session['username'] = login_data['username']
    else:
        resposta_do_DB = login_user_part2(login_data)

    if resposta_do_DB == True:
        session['authenticated'] = True
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": " tentativa de Login mal-sucedida."})
    

@app.route('/Register_New_Account', methods=['POST'])
def Create_Account():
    # Capturar os dados enviados no corpo da requisição
    New_account_data = request.get_json()

    resposta_do_DB = register_user(New_account_data)

    return resposta_do_DB


@app.route('/protected')
def protected():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return 'Você está autenticado!'

if __name__ == '__main__':
    app.run(debug=True)

