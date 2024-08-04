from flask import Flask, render_template, redirect, url_for, request, session, flash
from forms import LoginForm, TwoFactorForm
from logs import log_register
import pyotp

app = Flask(__name__)


app.secret_key = 'supersecret_key' # Necessário para usar sessões

# Usuário e senha de exemplo
USER_DATA = {
    "username": "testuser",
    "password": "password123",
    "2fa_secret": pyotp.random_base32()
}

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username == USER_DATA['username'] and password == USER_DATA['password']:
            session['username'] = username
            return redirect(url_for('two_factor'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')

    # Registra o log e renderiza a tela de login
    log_register()
    return render_template('login.html', form=form)

@app.route('/two-factor', methods=['GET', 'POST'])
def two_factor():
    form = TwoFactorForm()
    if 'username' not in session:
        return redirect(url_for('login'))

    if form.validate_on_submit():
        otp = form.otp.data
        totp = pyotp.TOTP(USER_DATA['2fa_secret'])

        if totp.verify(otp):
            session['authenticated'] = True
            return redirect(url_for('protected'))
        else:
            flash('Código 2FA inválido. Tente novamente.', 'danger')

    # Registra o log e renderiza a tela de 2FA
    return render_template('2fa.html', form=form)

@app.route('/protected')
def protected():
    if 'authenticated' not in session:
        return redirect(url_for('login'))
    return 'Você está autenticado!'

if __name__ == '__main__':
    app.run(debug=True)

