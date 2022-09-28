import pika
import json
import uuid
import time

class Loja:
    def __init__(self, nome):
        self.nome = nome
        self.produtos = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='reposicao')

        self.id = None
        result = self.channel.queue_declare(queue='this', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def __del__(self):
        self.connection.close()
    
    def on_response(self, ch, method, properties, body):
        print(body, self.id, properties.correlation_id)
        if self.id == properties.correlation_id:
            print('chegou:', body)
    
    def adiciona_produto(self, id, nome, quantidade):
        if quantidade >= 100:
            classe = "A"

        elif quantidade >= 60:
            classe = "B"

        else:
            classe = "C"

        produto = { "id": id, "nome": nome, "quantidade": quantidade, "classe": classe }
        self.produtos.append(produto)
    
    def vender(self, id, quantidade):
        item = next(item for item in self.produtos if item['id'] == id)

        if (item['quantidade'] - quantidade) < 0:
            print("Estoque insuficiente")
            return

        else:
            item['quantidade'] -= quantidade
            farol = self.checa_estoque(item)

            if farol == "vermelho":
                referencia = self.referencia_classe(item)
                reabastecimento = referencia - item['quantidade']

                self.id = str(uuid.uuid4())

                pedido = { "id": item['id'], "quantidade": reabastecimento }
                self.channel.basic_publish(
                    exchange='',
                    routing_key='reposicao',
                    properties=pika.BasicProperties(
                        reply_to=self.callback_queue,
                        correlation_id=self.id,
                    ),
                    body=json.dumps(pedido)
                )
                
                self.connection.process_data_events(time_limit=None)

            return

    def checa_estoque(self, item):
        if item['classe'] == "A":
            comparacao = 100
        elif item['classe'] == "B":
            comparacao = 60
        else:
            comparacao = 20

        porcentagem = item['quantidade'] * 100 / comparacao
        
        if porcentagem >= 50:
            return "verde"

        elif porcentagem >= 25:
            return "amarelo"

        return "vermelho"

    def referencia_classe(self, produto):
        if produto['classe'] == "A":
            return 100
        elif produto['classe'] == "B":
            return 60
        return 20