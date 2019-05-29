import os

import flask
import pymongo

app = flask.Flask(__name__)

client = pymongo.MongoClient()
db = client.users

@app.route('/hello-world')
def hello_world():
    return 'hello, world'

####################################################
#   API
####################################################

# funcao global para servir às funcoes GET
def filtrar_usuario(u, n):
    return {
        'id': n + 1,
        'nome': u['nome'],
        'email': u['email']
    }

@app.route('/users', methods=[ 'GET' ])
def get_users():

    users = db.users.find().sort('_id', pymongo.ASCENDING)
    users = list(
        filtrar_usuario(u, n) for n, u in enumerate(users)
    )

    return flask.jsonify(users)

@app.route('/users', methods=[ 'POST' ])
def post_user():

    form = flask.request.get_json()

    if not form:
        return 'Mensagem invalida!'

    nome = form ['nome']
    email = form['email']
    senha = form['senha']

    db.users.insert({
        'nome': nome,
        'email': email,
        'senha': senha
    })

    return flask.jsonify({
        'mensagem': 'usuario cadastrado!'
    })

@app.route('/users/auth', methods=[ 'GET' ])
def auth_user():
    return 'Autentica usuarios'

@app.route('/users/<int:userid>', methods=[ 'GET' ])
def get_user_by_id(userid):

    userid = userid - 1
    users = db.users.find().sort('_id', pymongo.ASCENDING)

    try:    
        u = filtrar_usuario(users[userid], userid)
        return flask.jsonify(u)
    except IndexError:
        return flask.jsonify({
            'mensagem': 'usuario não encontrado'
        }), 404

@app.route('/users/<int:userid>', methods=[ 'PUT' ])
def put_user_by_id(userid):
    
    userid = userid - 1
    users = db.users.find().sort('_id', pymongo.ASCENDING)

    user = None

    try:    
        user = users[userid]
    except IndexError:
        return flask.jsonify({
            'mensagem': 'usuario não encontrado'
        }), 404

    form = flask.request.get_json()

    if not form:
        return 'Mensagem invalida!'

    user['nome'] = form.get('nome') or user['nome']
    user['email'] = form.get('email') or user['email']
    user['senha'] = form.get('senha') or user['email']

    old_email = user['email']

    db.users.update({
        'email': old_email
    },user)

    return flask.jsonify({
        'mensagem': 'usuario atualizado!'
    })


@app.route('/users/<int:userid>', methods=[ 'DELETE' ])
def delete_user_by_id(userid):

    userid = userid - 1
    users = db.users.find().sort('_id', pymongo.ASCENDING)

    user = None

    try:    
        user = users[userid]
    except IndexError:
        return flask.jsonify({
            'mensagem': 'usuario não encontrado'
        }), 404

    db.users.remove({
        'email': user['email']
    })

    return flask.jsonify({
        'mensagem': 'usuario Deletado!'
    })

####################################################
#   VIEW
####################################################

@app.route('/', methods=[ 'GET' ])
def index():
    return flask.render_template('index.html', contexto={
        'nome': '',
        'mensagem': ''
    })

@app.route('/',methods=[ 'POST' ])
def post_index():

    form = flask.request.form

    return flask.render_template('index.html', contexto={
        'nome': form['nome'],
        'mensagem': 'Eae,mano!'
    })

if __name__ == '__main__':

#    os.environ['FLASK_APP'] = 'app.py'
#    os.environ['FLASK_ENV'] = 'development'

    app.run(debug=True)
