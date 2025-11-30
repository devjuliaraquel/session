from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_e_unica'

USUARIOS = {
    "aluno1": {
        "senha": "123",
        "nome": "João da Silva",
        "perfil": "Aluno",
        "dados_extra": "Matrícula: 2023001 | Curso: ADS"
    },
    "professora": {
        "senha": "456",
        "nome": "Maria de Souza",
        "perfil": "Professor(a)",
        "dados_extra": "Departamento: Computação | Carga Horária: 20h"
    },
    "coord": {
        "senha": "789",
        "nome": "Ana Oliveira",
        "perfil": "Coordenação",
        "dados_extra": "Área: Projetos | Ramal: 1001"
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USUARIOS and USUARIOS[username]['senha'] == password:

            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')

    return render_template('login.html', titulo="Login de Usuário")

@app.route('/perfil')
def perfil():
    # 1. Verifica se há um usuário logado na sessão
    if 'username' in session:
        username = session['username']
        # 2. Busca todos os dados do perfil na estrutura de dados
        dados_usuario = USUARIOS.get(username)

        # 3. Renderiza a tela de perfil com os dados específicos do usuário
        return render_template('perfil.html', usuario=dados_usuario)
    else:
        # 4. Se não estiver logado, redireciona para o login
        flash('Acesso restrito. Faça login.', 'warning')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Remove o username da sessão, deslogando o usuário
    session.pop('username', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# ROTA PADRÃO (REDIRECIONA PARA O LOGIN)
@app.route('/')
def index():
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True)
