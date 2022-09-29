import pika
import json
import uuid
import time

DEBUG = False

produtos_file = open('produtos_cd.json')
itens_no_estoque = json.load(produtos_file)

class Fabrica:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.produtos = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fabrica')

        self.queue_id = None
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.channel.basic_consume(queue='fabrica', auto_ack=True, on_message_callback=self.callback)

    def callback(self, body):
        decoded = body.decode()

        if decoded == self.produtos.id:

            produto_encontrado = next(item for item in itens_no_estoque if item['id'] == pedido['id'])
            produto_encontrado['quantidade'] += 100

    def __del__(self):
        self.connection.close()
    
    def adiciona_produto(self, id, nome):
        produto = { 'id': id, 'nome': nome}
        self.produtos.append(produto)