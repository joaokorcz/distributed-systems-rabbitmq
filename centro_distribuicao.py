#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

pedido = []
dicio = {}
def callback(ch, method, properties, body):
    
    body_or = body
    print('Recebido:', body)
    string = body.decode().split(", ")
    item = string[0][6:]
    quantidade = string[1][12:]
    quantidade = int(quantidade)
    pedido.append(body)

    dicio = {"item": item, "quantidade": quantidade}
    
    pedido.append(body)
    channel.basic_publish(exchange='', routing_key='fabrica', body=body_or)


channel.basic_consume(queue='reposicao', auto_ack=True, on_message_callback=callback)

channel.start_consuming()