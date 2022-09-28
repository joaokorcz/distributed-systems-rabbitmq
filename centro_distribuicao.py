#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

itens_no_estoque = []

def callback(ch, method, properties, body):
    decoded = body.decode()
    pedido = json.loads(decoded)
    print(pedido)

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id = properties.correlation_id
        ),
        body='toma de volta')

    ch.basic_ack(delivery_tag=method.delivery_tag)

    #channel.basic_publish(exchange='', routing_key='fabrica', body=pedido)


channel.basic_consume(queue='reposicao', on_message_callback=callback)

channel.start_consuming()