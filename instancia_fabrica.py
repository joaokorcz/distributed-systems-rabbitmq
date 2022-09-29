#!/usr/bin/env python
import pika
import json
from Fabrica import Fabrica

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

fabrica_file = open('fabricas.json')
fabricas = json.load(fabrica_file)

produtos_file = open('produtos_cd.json')
itens_no_estoque = json.load(produtos_file)

instancias = []

for fabrica in fabricas:
    nova_fabrica = Fabrica(fabrica['id'], fabrica['nome'])
    print(fabrica['nome'])
    for produto in fabrica['produtos']:
        nova_fabrica.adiciona_produto(produto['id'], produto['nome'])
    instancias.append(nova_fabrica)

for instancia in instancias:
    instancia.start_consume()

