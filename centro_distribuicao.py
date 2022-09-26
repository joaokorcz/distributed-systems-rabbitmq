#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

def callback(ch, method, properties, body):
    print('Recebido:', body)

channel.basic_consume(queue='reposicao', auto_ack=True, on_message_callback=callback)

channel.start_consuming()