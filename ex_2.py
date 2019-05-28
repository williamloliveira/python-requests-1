
import requests

# Criar um programa que lista todos os 
# usuários da api

API_URL = 'https://gen-net.herokuapp.com/api/users'

# response = requests.get(API_URL)

# users = response.json()
# for u in users:
#     print(u)

# Criar um programa que ajude o usuário a se cadastrar
# Verificar o STATUS da requisição

user_id = None

user = {
    'name': input('Digite seu nome: '),
    'email': input('Digite seu email: '),
    'password': input('Digite sua senha: ')
}
response = requests.post(API_URL, json=user)

print(type(response))

if response.status_code == 200:
    user_id = response.json()['id']
    print(user_id)
else:
    print('Erro ao cadastrar')

# Buscar UM usuário pelo id
response = requests.get(API_URL + '/{}'.format(user_id))
print(response.json())

new_email = 'test_' + str(user_id) + '@test.com'
response = requests.put(API_URL + '/{}'.format(user_id), json={
    'email': new_email      
})

if response.status_code == 200:
    print(response.json())

response = requests.post(API_URL + '/auth', {
    'email': new_email,
    'password': user['password']
})

print(response.json())

response = requests.delete(API_URL + '/{}'.format(user_id))
print(response.status_code)