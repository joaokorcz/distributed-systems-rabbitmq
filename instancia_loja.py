#!/usr/bin/env python
from Loja import Loja

americanas = Loja("Americanas")
americanas.adiciona_produto("Notebook", 2)
americanas.remove_produto("Notebook", 2)

""" def callback(ch, method, properties, body):
    print('Recebido:', body)

channel.basic_consume(queue='fabrica', auto_ack=True, on_message_callback=callback)
channel.start_consuming() """