#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='reposicao')

class Loja:
    def __init__(self, nome):
        self.nome = nome
        self.produtos = []
    
    def adiciona_produto(self, nome, quantidade):
        if quantidade >= 100:
            classe = "A"

        elif quantidade >= 60:
            classe = "B"

        else:
            classe = "C"

        produto = { "nome": nome, "quantidade": quantidade, "classe": classe }
        self.produtos.append(produto)
    
    def remove_produto(self, nome, quantidade):
        #index = next((index for (index, d) in enumerate(self.produtos) if d["nome"] == nome), None)
        item = next(item for item in self.produtos if item['nome'] == nome)

        if (item['quantidade'] - quantidade) < 0:
            print("Estoque insuficiente")
            return

        else:
            item['quantidade'] -= quantidade
            farol = self.checa_estoque(nome)

            if farol == "vermelho":
                referencia = self.referencia_classe(item)
                reabastecimento = referencia - item['quantidade']

                pedido = { "nome": self.nome, "quantidade": reabastecimento }
                channel.basic_publish(exchange='', routing_key='reposicao', body=json.dumps(pedido))

            return

    def checa_estoque(self, nome):
        item = next(item for item in self.produtos if item['nome'] == nome)

        if item['classe'] == "A":
            comparacao = 100
        elif item['classe'] == "B":
            comparacao = 60
        else:
            comparacao = 20

        porcentagem = item['quantidade'] * 100 / comparacao
        
        if porcentagem >= 50:
            return "verde"

        elif porcentagem >= 25:
            return "amarelo"

        return "vermelho"

    def referencia_classe(self, produto):
        if produto['classe'] == "A":
            return 100
        elif produto['classe'] == "B":
            return 60
        return 20

americanas = Loja("Americanas")
americanas.adiciona_produto("Notebook", 2)
americanas.remove_produto("Notebook", 2)

""" def callback(ch, method, properties, body):
    print('Recebido:', body)

channel.basic_consume(queue='fabrica', auto_ack=True, on_message_callback=callback)
channel.start_consuming() """

connection.close()
