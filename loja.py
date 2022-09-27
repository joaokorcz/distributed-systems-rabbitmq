#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

class Loja:
    def __init__(self, nome):
        self.nome = nome
        self.produto = []
    
    def adiciona_produto(self, nome, quantidade):
        if quantidade >= 100:
            classe = "A"

        elif quantidade >= 60:
            classe = "B"

        else:
            classe = "C"

        produto = {"nome": nome, "quantidade": quantidade, "classe": classe}
        self.produto = self.produto.append(produto)
    
    def remove_produto(self, nome, quantidade):
        #index = next((index for (index, d) in enumerate(self.produto) if d["nome"] == nome), None)
        item = next(item for item in self.produto if item['nome'] == nome)

        if (item['quantidade'] - quantidade) <= 0:
            print("Estoque insuficiente")
            return

        else:
            item['quantidade'] -= quantidade
            farol = self.checa_estoque(nome)

            if farol == "vermelho":
                pedido = # ENVIAR NOME E QUANTIDADE, CALCULAR A QUANTIDADE COM BASE NA PORCENTAGEM DA CLASSE
                channel.basic_publish(exchange='', routing_key='reposicao', body=pedido)

            return

    def checa_estoque(self, nome):
        item = next(item for item in self.produto if item['nome'] == nome)
        farol = item.quantidade * 100

        # FALTANDO IMPLEMENTAR
        if item.classe == "A":
            porcentagem = farol / 100

        elif item.classe == "B":
        
        else:

pedido = "item: iPhone, quantidade: 30"

americanas = Loja("Americanas")

def callback(ch, method, properties, body):
    
    print('Recebido:', body)

channel.basic_consume(queue='fabrica', auto_ack=True, on_message_callback=callback)

channel.start_consuming()

channel.basic_publish(exchange='', routing_key='reposicao', body=pedido)

print("Enviando pedido de iPhone!")

connection.close()
