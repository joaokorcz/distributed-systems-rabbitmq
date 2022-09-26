#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

pedido = "item: iPhone, quantidade: 30"

channel.basic_publish(exchange='', routing_key='reposicao', body=pedido)

print("Enviando pedido de iPhone!")

connection.close()
