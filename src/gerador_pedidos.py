import argparse
import random
import datetime
import json
import boto3
import sys
import time
import uuid
from faker import Faker

fake = Faker()

class PedidoDeCompra:
    def __init__(self, produto, valor_unitario, quantidade, data_criacao, pais, id_cliente):
        self.id_pedido = str(uuid.uuid4())  # adiciona um identificador único a cada pedido
        self.produto = produto
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade
        self.data_criacao = data_criacao.isoformat()
        self.pais = pais
        self.id_cliente = id_cliente

    def to_dict(self):
        return self.__dict__

produtos = {
    "TV": 2500,
    "GELADEIRA": 2000,
    "HOMETHEATER": 500,
    "COMPUTADOR": 700,
    "MONITOR": 600,
    "TABLET": 1100,
    "SOUNDBAR": 900,
    "CELULAR": 1000,
    "NOTEBOOK": 1500
}

paises = ["BR", "US", "AR"]

def gerar_pedido_aleatorio():
    produto, valor_unitario = random.choice(list(produtos.items()))
    quantidade = random.randint(1, 3)
    data_criacao = datetime.datetime.now().replace(day=random.randint(1, datetime.datetime.now().day), hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))
    pais = random.choice(paises)
    id_cliente = fake.unique.random_number(digits=5)
    return PedidoDeCompra(produto, valor_unitario, quantidade, data_criacao, pais, id_cliente)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destino", default="arquivo", help="Destino dos pedidos gerados")
    parser.add_argument("--quantidade", default=50, help="Quantidade de pedidos gerados")
    args = parser.parse_args()

    print("Destino dos dados:", args.destino)
    print("Quantidade de pedidos:", args.quantidade)

    destino = args.destino.lower()
    quantidade = int(args.quantidade)

    if destino == "arquivo":
        arquivo = open("pedidos.txt", "w")  # abre o arquivo para escrita
        for _ in range(quantidade): 
            pedido = gerar_pedido_aleatorio()
            arquivo.write(json.dumps(pedido.to_dict()) + "\n")  # escreve o pedido no arquivo
        arquivo.close()  # fecha o arquivo
    elif destino == "kinesis":
        kinesis = boto3.client('kinesis')  
        stream_name = 'pedidos'  

        for _ in range(quantidade): 
            pedido = gerar_pedido_aleatorio()
            kinesis.put_record(
                StreamName=stream_name,
                Data=json.dumps(pedido.to_dict()),
                PartitionKey=str(pedido.id_pedido)
            )
            time.sleep(0.1)  # pausa por 1 segundo
    else:
        print("Destino inválido")
        sys.exit(1)

if __name__ == '__main__':
    main()