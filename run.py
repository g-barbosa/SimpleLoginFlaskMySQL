from runbanco import *
from flask import Flask, render_template, redirect, url_for, request, session
import os

app =Flask(__name__)
app.secret_key = 'gbbdev'

app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__))+'/uploads'

#redireciona para pagina de login
@app.route('/')
def index():
    return redirect(url_for('login'))

#Verifica se o user ja está logado.Caso sim, o redireciona diretamente para home
#Caso não,realiza o login verificando se o user e o pass digitado existem no banco de dados, caso contrario, apresenta erro
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = verificaUser(request.form['username'])
        senha = user[2]
        
        if request.form['username'] != user[1] or request.form['password'] != senha:
            error = 'Usuario ou senha incorretos, tente novamente.'
        else:
            session['usuario_logado'] = user[3]
            return redirect(url_for('home'))
            
    return render_template('index.html')

#pagina inicial onde verifica se o usuario esta logado, caso contrario o redireciona para pagina de login
@app.route('/home')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    else:
        nome = session['usuario_logado']
        return render_template('pagina.html',nome=nome)

#sai da sessao, nao permitindo o usuario entrar em home ate que faça login novamente
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['usuario_logado'] = None
    return redirect(url_for('index'))

if __name__ == ('__main__'):
    app.run(debug=True,host='0.0.0.0',port=8080)
