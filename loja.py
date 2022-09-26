#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

channel.basic_publish(exchange='', routing_key='reposicao', body='preciso de 30 iPhones')

print("Enviando pedido de iPhone!")

connection.close()
