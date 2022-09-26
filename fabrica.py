#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fabrica')

fabricas = {}

def callback(ch, method, properties, body):

    fabricas = {"nome":"Nestle", "produtos": {{"produto": "cafe", "quantidade": 30}, {"produto":"leite", "quantidade":40}}}
    
    print('Recebido:', body)

channel.basic_consume(queue='fabrica', auto_ack=True, on_message_callback=callback)

channel.start_consuming()