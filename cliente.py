from os import terminal_size
import socket
import threading

nomeUsuario = input("Escolha seu nome de usuário: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Função que recebe
def recebe():
    while True:
        try: 
            mensagem = cliente.recv(1024).decode('ascii')
            if mensagem == 'NOME':
                cliente.send(nomeUsuario.encode('ascii'))
            else:
                print(mensagem)
        except:
            print("Ocorreu um erro!")
            cliente.close()
            break

def escreve():
    while True:
        # Mensagem para o servidor
        message = f'{nomeUsuario}: {input("")}'
        cliente.send(message.encode('ascii'))

receive_thread = threading.Thread(target=recebe)
receive_thread.start()

whrite_thread = threading.Thread(target=escreve)
whrite_thread.start()
