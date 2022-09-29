#!/usr/bin/env python
from Loja import Loja
import json

instancias = []

lojas_file = open('lojas.json')
lojas = json.load(lojas_file)
for loja in lojas:
    nova_loja = Loja(loja['nome'])
    for produto in loja['produtos']:
        nova_loja.adiciona_produto(produto['id'], produto['nome'], produto['classe'], produto['quantidade'])
    instancias.append(nova_loja)
    
instancias[0].vender(1, 8)
