#!/usr/bin/env python
from Loja import Loja
import json
from colorama import Fore

instancias = []

lojas_file = open('lojas.json')
lojas = json.load(lojas_file)
for loja in lojas:
    nova_loja = Loja(loja['id'], loja['nome'])
    for produto in loja['produtos']:
        nova_loja.adiciona_produto(produto['id'], produto['nome'], produto['classe'], produto['quantidade'])
    instancias.append(nova_loja)
    
def selecionar_loja(instancias):
    print('-- Menu de lojas --')
    for loja in instancias:
        print(f'** { loja.id } - { loja.nome }')
    print('** 0 - \u001b[36mSair\u001b[37m')

    id_selecionado = int(input('\n>> Escolha uma loja pelo número: '))

    try:
        loja = next(loja for loja in instancias if loja.id == id_selecionado)

        print('-- Loja selecionada:', loja.nome + '\n') 

        return loja

    except:
        if id_selecionado == 0:
            return 'sair'
        print('\n## ERRO\n')
        return False

def realizar_compra(loja):
    print('-- Catálogo', loja.nome)
    for produto in loja.produtos:
        cor = Fore.GREEN
        if produto['farol'] == 'amarelo':
            cor = Fore.YELLOW
        elif produto['farol'] == 'vermelho':
            cor = Fore.RED


        print(f'** { produto["id"] } - { cor + produto["nome"] + Fore.WHITE}')
    
    id_selecionado = int(input('\n>> Escolha um produto pelo número: '))

    try:
        produto = next(produto for produto in loja.produtos if produto['id'] == id_selecionado)

        print('-- Produto selecionado:', produto['nome'] + '\n')

        print('-- Estoque disponível:', produto['quantidade'])
        quantidade = int(input('>> Escolha a quantidade: '))

        if loja.vender(id_selecionado, quantidade):
            print('-- Você comprou', quantidade, 'unidades de', produto['nome'] + '\n')
        else:
            print('## Estoque insuficiente\n')
    
    except:
        print('\n## ERRO\n')

loja_selecionada = True
while loja_selecionada != 'sair':
    loja_selecionada = selecionar_loja(instancias)
    if loja_selecionada and loja_selecionada != 'sair':
        realizar_compra(loja_selecionada)
