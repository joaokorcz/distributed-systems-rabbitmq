import pika
import json
import uuid
import time

DEBUG = False

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

    def __del__(self):
        self.connection.close()
    
    def adiciona_produto(self, id, nome):
        produto = { 'id': id, 'nome': nome}
        self.produtos.append(produto)