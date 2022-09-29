#!/usr/bin/env python
import pika
import json

DEBUG = False

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reposicao')

produtos_file = open('produtos_cd.json')
itens_no_estoque = json.load(produtos_file)

def callback(ch, method, properties, body):
    if DEBUG: print(body)
    decoded = body.decode()
    pedido = json.loads(decoded)
    print('Recebemos um pedido de reposição...')
    print('    id do produto:', pedido['id'])

    produto_encontrado = next(item for item in itens_no_estoque if item['id'] == pedido['id'])
    
    if produto_encontrado['quantidade'] >= pedido['quantidade']:
        body = { 'estoque': 'sim', 'id': pedido['id'] ,'quantidade': pedido['quantidade'] }
        print('    temos estoque suficiente: sim')
        print('    quantidade atual:', produto_encontrado['quantidade'])
        produto_encontrado['quantidade'] -= pedido['quantidade']
        print('    nova quantidade:', produto_encontrado['quantidade'])
    else:
        print('    temos estoque suficiente: nao')
        body = { 'estoque': 'nao', 'id': pedido['id'], 'quantidade': 0 }

    print('Enviando resposta para o produto de id', pedido['id'])

    if body.estoque == 'nao':
        body.quantidade = 100

        ch.basic_publish(
        exchange='',
        routing_key='fabrica',
        properties=pika.BasicProperties(
            correlation_id = properties.correlation_id
        ), 
        body=json.dumps(body))

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id = properties.correlation_id
        ),
        body=json.dumps(body))

    ch.basic_ack(delivery_tag=method.delivery_tag)

    #channel.basic_publish(exchange='', routing_key='fabrica', body=pedido)


channel.basic_consume(queue='reposicao', on_message_callback=callback)

channel.start_consuming()