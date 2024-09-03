from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from logs import log_register
from DB import register_user, login_user_part2, login_user_part1, grab_secret_question
import pyotp

app = Flask(__name__)


app.secret_key = 'supersecret_key' # Necessário para usar sessões


#  Pagina inicial
@app.route('/', methods=['GET', 'POST'])
def render_login():
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


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/nothing_here', methods=['GET'])
def render_console():
    return render_template('console.html')

@app.route('/protected')
def protected():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return 'Você está autenticado!'

if __name__ == '__main__':
    app.run(debug=True)

