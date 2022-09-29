#!/usr/bin/env python
from Loja import Loja
import json

instancias = []

lojas_file = open('lojas.json')
lojas = json.load(lojas_file)
for loja in lojas:
    print(loja['id'])
    nova_loja = Loja(loja['id'], loja['nome'])
    for produto in loja['produtos']:
        nova_loja.adiciona_produto(produto['id'], produto['nome'], produto['classe'], produto['quantidade'])
    instancias.append(nova_loja)
    
def selecionar_loja(instancias):
    print('-- Menu de lojas --')
    for loja in instancias:
        print(f'** { loja.id } - { loja.nome }')

    id_selecionado = int(input('\n-- Escolha uma loja pelo número: '))

    loja = next(loja for loja in instancias if loja.id == id_selecionado)

    print('-- Loja selecionada:', loja.nome)

    return loja

def apresentar_catalogo(loja):
    print('-- Catálogo', loja.nome, '--')
    for produtos in loja.produtos:
        print(f'** { produto["id"] } - { produto["nome"] }')
    
loja_selecionada = selecionar_loja(instancias)
apresentar_catalogo(loja_selecionada)

