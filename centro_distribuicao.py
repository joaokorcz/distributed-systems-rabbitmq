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
global queue_id


def on_response(ch, method, properties, body):
    if DEBUG:
        print(body)
    if queue_id == properties.correlation_id:
        decoded = body.decode()
        response = json.loads(decoded)

        item = next(item for item in itens_no_estoque if item['id'] == response['id_produto'])
        item['quantidade'] += response['quantidade']
        print('Recebemos da fábrica', response['quantidade'], 'unidades do produto de id:', item['id'])

channel.basic_consume(
    queue=callback_queue,
    on_message_callback=on_response,
    auto_ack=True
)

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

    if body['estoque'] == 'nao':
        global queue_id
        queue_id = str(uuid.uuid4())
        print("QUEUE ID:", queue_id)
        ch.basic_publish(
            exchange='',
            routing_key='fabrica',
            properties=pika.BasicProperties(
                        reply_to=callback_queue,
                        correlation_id=queue_id,
            ),
            body=json.dumps(pedido['id'])
        )

       # ch.connection.process_data_events(time_limit=None)
        
    print('Enviando resposta para o produto de id', pedido['id'])

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(body))


    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='reposicao', on_message_callback=callback)

channel.start_consuming()
