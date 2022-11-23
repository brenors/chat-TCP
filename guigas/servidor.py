import socket as s
import threading

HOST = '127.0.0.1'
PORT = 9999

servidor = s.socket(s.AF_INET, s.SOCK_STREAM)
servidor.bind((HOST, PORT))

servidor.listen()

clientes = []
nomes = []


def broadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)


def handle(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            print(f"{nomes[clientes.index(cliente)]} diz {mensagem}")
            broadcast(mensagem)
        except:
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nome = nomes[index]
            nomes.remove(nome)
            break


def receber():
    while True:
        cliente, endereco = servidor.accept()
        print(f"Conectado com {str(endereco)}")

        cliente.send("NICK".encode('utf-8'))
        nome = cliente.recv(1024)

        nomes.append(nome)
        clientes.append(cliente)

        print(f"Nome do cliente: {nome}")
        broadcast(f"{nome} conectou no servidor!\n".encode('utf-8'))
        cliente.send("Conectado no servidor!\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()


print("Servidor rodando...")
receber()
