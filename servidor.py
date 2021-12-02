import threading
import socket 

# Definindo endereço do servidor
host = '127.0.0.1' #localhost
port = 55555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))

# Servidor começa a escutar
servidor.listen()

clientes = []
nomeUsuariosList = []

def broadcast(message):
    for cliente in clientes:
        cliente.send(message)

def handle(cliente):
    while True:
        try:
            # Envia mensagem para todos no servidor
            message = cliente.recv(1024)
            broadcast(message)
        except:
            # Cliente sai da conversa
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nomeUsuario = nomeUsuariosList[index]
            broadcast(f'{nomeUsuario} deixou a conversa!'.encode('ascii'))
            nomeUsuariosList.remove(nomeUsuario)
            break

def recebe():
    while True:
        # Adiciona o cliente na conversa
        cliente, address = servidor.accept()
        print(f"Conectado no endereço: {str(address)}")

        cliente.send('NOME'.encode('ascii'))
        nomeUsuario = cliente.recv(1024).decode('ascii')
        nomeUsuariosList.append(nomeUsuario)
        clientes.append(cliente)

        print(f'O nome de usuário do cliente é {nomeUsuario}!')
        broadcast(f'{nomeUsuario} se juntou a conversa!'.encode('ascii'))
        cliente.send('Conectado ao servidor!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()

print("Servidor iniciado e ouvindo...")
recebe()
