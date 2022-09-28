import pika
import json

class Loja:
    def __init__(self, nome):
        self.nome = nome
        self.produtos = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='reposicao')

    def __del__(self):
        self.connection.close()
    
    def adiciona_produto(self, nome, quantidade):
        if quantidade >= 100:
            classe = "A"

        elif quantidade >= 60:
            classe = "B"

        else:
            classe = "C"

        produto = { "nome": nome, "quantidade": quantidade, "classe": classe }
        self.produtos.append(produto)
    
    def remove_produto(self, nome, quantidade):
        #index = next((index for (index, d) in enumerate(self.produtos) if d["nome"] == nome), None)
        item = next(item for item in self.produtos if item['nome'] == nome)

        if (item['quantidade'] - quantidade) < 0:
            print("Estoque insuficiente")
            return

        else:
            item['quantidade'] -= quantidade
            farol = self.checa_estoque(nome)

            if farol == "vermelho":
                referencia = self.referencia_classe(item)
                reabastecimento = referencia - item['quantidade']

                pedido = { "nome": item['nome'], "quantidade": reabastecimento }
                self.channel.basic_publish(exchange='', routing_key='reposicao', body=json.dumps(pedido))

            return

    def checa_estoque(self, nome):
        item = next(item for item in self.produtos if item['nome'] == nome)

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