import pika
import json
import uuid
import time

DEBUG = False

class Loja:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.produtos = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='reposicao')

        self.queue_id = None
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def __del__(self):
        self.connection.close()
    
    def on_response(self, ch, method, properties, body):
        if DEBUG: print(body)
        if self.queue_id == properties.correlation_id:
            decoded = body.decode()
            resposta = json.loads(decoded)
            print('LOJA AVISA: Pedido de reposição respondido...')
            print('    havia estoque suficiente no cd:', resposta['estoque'])
            print('    id do produto:', resposta['id'])
            print('    quantidade recebida:', resposta['quantidade'])

        item = next(item for item in self.produtos if item['id'] == resposta['id'])
        item['quantidade'] += resposta['quantidade']
    
    def adiciona_produto(self, id, nome, classe, quantidade):
        produto = { 'id': id, 'nome': nome, 'quantidade': quantidade, 'classe': classe }
        self.produtos.append(produto)
    
    def vender(self, id, quantidade):
        item = next(item for item in self.produtos if item['id'] == id)

        if (item['quantidade'] - quantidade) < 0:
            return False

        else:
            item['quantidade'] -= quantidade
            farol = self.checa_estoque(item)

            if farol == 'vermelho':
                print('LOJA AVISA: com essa compra, estoque de', item['nome'] + ' ficou vermelho...')
                print('    Fazendo pedido de reposição...')
                referencia = self.referencia_classe(item)
                reabastecimento = referencia - item['quantidade']

                self.queue_id = str(uuid.uuid4())

                pedido = { 'id': item['id'], 'quantidade': reabastecimento }
                self.channel.basic_publish(
                    exchange='',
                    routing_key='reposicao',
                    properties=pika.BasicProperties(
                        reply_to=self.callback_queue,
                        correlation_id=self.queue_id,
                    ),
                    body=json.dumps(pedido)
                )
                
                self.connection.process_data_events(time_limit=None)

                print('LOJA AVISA: Nova quantidade do produto', item['nome'] + ':', item['quantidade'])

            return True

    def checa_estoque(self, item):
        if item['classe'] == 'A':
            comparacao = 100
        elif item['classe'] == 'B':
            comparacao = 60
        else:
            comparacao = 20

        porcentagem = item['quantidade'] * 100 / comparacao
        
        if porcentagem >= 50:
            return 'verde'

        elif porcentagem >= 25:
            return 'amarelo'

        return 'vermelho'

    def referencia_classe(self, produto):
        if produto['classe'] == 'A':
            return 100
        elif produto['classe'] == 'B':
            return 60
        return 20