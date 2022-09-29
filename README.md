# distributed-systems-rabbitmq

# requisitos
  - docker e docker-compose
  - python3
  - pip para instalação de pacotes

# execução

certifique-se que os comandos `python` utilizam python 3.

- na pasta do projeto: `docker-compose up -d`
- instale as dependencias: `pip install -r requirements.txt`
- no mesmo terminal: `python instancia_loja.py`
  - este terminal será usado para fazer as compras nas 20 lojas
- em outro terminal: `python centro_distribuicao.py`
- em outro terminal: `python instancia_fabrica.py`
