
import requests


# Criar um programa que peça que o usuário
# digite o cep dele e imprimao endereço

cep = input('Digite seu cep: ')

VIACEP_URI = 'http://viacep.com.br/ws/{}/json/'.format(cep)

response = requests.get(VIACEP_URI)

print('Status Code', response.status_code)
print('Texto plano', response.text)
print('Dicionário do Python', response.json())