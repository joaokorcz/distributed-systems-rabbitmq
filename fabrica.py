#!/usr/bin/env python
import pika
import json
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fabrica')

fabrica_file = open('fabricas.json')
fabricas = json.load(fabrica_file)

produtos_file = open('produtos_cd.json')
itens_no_estoque = json.load(produtos_file)

def callback(ch, method, properties, body):

    decoded = body.decode()
    pedido = json.loads(decoded)

    print('Recebemos um pedido...')
    print('    id do produto:', pedido['id'])
    print('    fábrica encontrada...')

    fabrica_encontrada = next(fabrica for fabrica in fabricas if fabrica['id'] == pedido['id'])

    print('    fabricando produtos...')

    produto_encontrado = next(item for item in itens_no_estoque if item['id'] == pedido['id'])
    produto_encontrado['quantidade'] += pedido['quantidade']

    print('    produto enviado para o centro de distribuição!')

channel.basic_consume(queue='fabrica', auto_ack=True, on_message_callback=callback)

channel.start_consuming()