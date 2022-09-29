#!/usr/bin/env python
import queue
import pika
import json
import uuid

DEBUG = False

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

produtos_file = open('produtos_cd.json')
itens_no_estoque = json.load(produtos_file)

fabrica_file = open('fabricas.json')
fabricas = json.load(fabrica_file)

result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue
queue_id = None

def callback(ch, method, properties, body):
    if DEBUG:
        print(body)
    decoded = body.decode()
    pedido = json.loads(decoded)
    print('Recebemos um pedido de reposição...')
    print('    id do produto:', pedido['id'])

    produto_encontrado = next(
        item for item in itens_no_estoque if item['id'] == pedido['id'])

    if produto_encontrado['quantidade'] >= pedido['quantidade']:
        body = {'estoque': 'sim',
                'id': pedido['id'], 'quantidade': pedido['quantidade']}
        print('    temos estoque suficiente: sim')
        print('    quantidade atual:', produto_encontrado['quantidade'])
        produto_encontrado['quantidade'] -= pedido['quantidade']
        print('    nova quantidade:', produto_encontrado['quantidade'])
    else:
        print('    temos estoque suficiente: nao')
        body = {'estoque': 'nao', 'id': pedido['id'], 'quantidade': 0}

    print('Enviando resposta para o produto de id', pedido['id'])

    if body.estoque == 'nao':
        queue_id = str(uuid.uuid4())

        ch.basic_publish(
            exchange='',
            routing_key='fabrica',
            properties=pika.BasicProperties(
                        reply_to=callback_queue,
                        correlation_id=queue_id,
            ),
            body=json.dumps(pedido['id'])
        )

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(body))

    ch.basic_ack(delivery_tag=method.delivery_tag)

    #channel.basic_publish(exchange='', routing_key='fabrica', body=pedido)


channel.basic_consume(queue='reposicao', on_message_callback=callback)

channel.start_consuming()
