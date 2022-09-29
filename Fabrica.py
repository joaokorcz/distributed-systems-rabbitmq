import pika
import json
import uuid
import time
import threading

DEBUG = False

produtos_file = open('produtos_cd.json')
itens_no_estoque = json.load(produtos_file)


class Fabrica:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.produtos = []
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='fabrica')

        self.channel.basic_consume(
            queue='fabrica', auto_ack=False, on_message_callback=self.callback)
                

    def start_consume(self):
        teste = threading.Thread(target=self.channel.start_consuming)
        teste.start()

    def callback(self, ch, method, properties, body):
        decoded = body.decode()
        temos = False
        for produto in self.produtos:
            print(produto)
            if produto['id'] == int(decoded):
                print("entrei")
                temos = True

        body = {"fabrica": self.nome, "id_produto": int(decoded), "quantidade": 100}
        if temos:
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id
                ),
                body=json.dumps(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)


    def __del__(self):
        self.connection.close()

    def adiciona_produto(self, id, nome):
        produto = {'id': id, 'nome': nome}
        self.produtos.append(produto)
