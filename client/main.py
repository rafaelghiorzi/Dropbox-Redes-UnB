import socket
import json
import os
import time
import mimetypes

# Configuração do servidor e cliente
#HOST = '0.0.0.0'
HOST = '127.0.0.1'

SERVER_PORT = 8080
CLIENT_PORT = 50000
USERNAME = None

# Funções do cliente
def login():
    global USERNAME
    os.system('cls')
    print('Login')
    print('Digite seu nome de usuário (sem espaços, apenas uma palavra):')
    username = input().strip()
    print('Digite sua senha (sem espaços, apenas uma palavra):')
    password = input().strip()
    
    body = json.dumps({ 'username': username, 'password': password })
    headers = f'POST /user/login  HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n'
    request = headers + body
    try:
        # Preparando o request
        body = json.dumps({ 'username': username, 'password': password })
        headers = (
            f'POST /user/login HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        request = headers + body
        
        # Criando e conectando a um socket dinâmico do computador
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        
        # enviando request
        client_socket.sendall(request.encode('utf-8'))
        
        # recebendo resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        if response.find('200') != -1:
            USERNAME = response.split('\r\n\r\n')[1]
            logged()
        else:
            print("Algo deu errado, tente novamente") 
            time.sleep(3)
            menu()      
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        print('Voltando para o menu...')
        time.sleep(5)
        menu()
    except Exception as e:
        print(f'Error: {str(e)}')
        print('Voltando para o menu...')
        time.sleep(5)
        menu()
    finally:
        client_socket.close()

def register():
    global USERNAME
    os.system('cls')
    print('Registrar')
    print('Digite seu nome de usuário (apenas uma palavra, sem espaços):')
    username = input()
    print('Digite sua senha (apenas uma palavra, sem espaços):')
    password = input()
    
    try:
        # Criando o request
        body = json.dumps({ 'username': username, 'password': password })
        headers = (
            f'POST /user/register HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        request = headers + body
        
        # Conectando o socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        
        # envio o request
        client_socket.sendall(request.encode('utf-8'))
        
        # resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        if response.find('201') != -1:
            USERNAME = response.split('\r\n\r\n')[1]
            logged()
        else:
            print("Algo deu errado, tente novamente") 
            time.sleep(3)
            menu()    
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        print('Voltando para o menu...')
        time.sleep(5)
        menu()
    except Exception as e:
        print(f'Error: {str(e)}')
        print('Voltando para o menu...')
        time.sleep(5)
        menu()
    finally:
        client_socket.close()

def menu():
    os.system('cls')
    print('1. Fazer login')
    print('2. Registrar usuário')
    print('3. para sair')

    option = input().strip()
    match option:
        case '1':
            login()
        case '2':
            register()
        case '3':
            os.system('cls')
            exit(0)
        case _:
            print('Selecione uma opção válida')
            time.sleep(2)
            menu()
            
def list_files():
    os.system('cls')
    try:
        # Preparando o request
        headers = (
            f'GET /files HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        
        # Criando e conectando a um socket dinâmico do computador
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        
        # enviando request
        client_socket.sendall(headers.encode('utf-8'))
        
        # recebendo resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')

        if response.find('200') == -1:
            print('Error: Could not list files')
            time.sleep(3)
            logged()
        
        lista = json.loads(response.split('\r\n\r\n')[1])
        print('Arquivos disponíveis:')
        
        # listando arquivos disponíveis
        for i in range(len(lista)):
            print(f'{i+1}. {lista[i][1]} - enviado por {lista[i][3]}')
            
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
    except Exception as e:
        print(f'Error: {str(e)}')
    finally:
        client_socket.close()
        input('Pressione ENTER para continuar...')
        logged()

def upload_file():
    global USERNAME
    os.system('cls')
    print('Upload de arquivo')
    print('Digite o caminho do arquivo:')
    filepath = input().strip('"')
    if not os.path.exists(filepath):
        print('Arquivo não encontrado')
        input('Pressione ENTER para continuar...')
        logged()
    
    filename = os.path.basename(filepath)
    mimetype, _ = mimetypes.guess_type(filepath)
    mimetype = mimetype or 'application/octet-stream'
    
    try:
        with open(filepath, 'rb') as file:
            file_data = file.read()
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'     
        metadata = {
            'name': filename,
            'path': filepath,
            'user_username': USERNAME
        }
        
        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="metadata"\r\n'
            f'Content-Type: application/json\r\n\r\n'
            f'{json.dumps(metadata)}\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f'Content-Type: {mimetype}\r\n\r\n'
        ).encode('utf-8') + file_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')
        
        headers = (
            f'POST /files/upload HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'Content-Type: multipart/form-data; boundary={boundary}\r\n'
            f'Content-Length: {len(body)}\r\n'
            f'\r\n'
        )
        
        request = headers.encode('utf-8') + body
        print('Enviando arquivo...')
        # Criando e conectando a um socket dinâmico do computador
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        #enviando request
        client_socket.sendall(request)
        #recebendo resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        print('\nServer response:')
        print(response)
        if response.find('201') != -1:
            os.system('cls')
            print('Arquivo enviado com sucesso para o servidor')
            time.sleep(3)
            logged()
        
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        print('Voltando para o menu...')
        time.sleep(3)
        logged()
    except Exception as e:
        print(f'Error: {str(e)}')
        print('Voltando para o menu...')
        time.sleep(3)
        logged()

def download_file():
    global USERNAME
    os.system('cls')
    try:
        # Prepara request da lista de arquivos
        headers = (
            f'GET /files HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.sendall(headers.encode('utf-8'))
        
        # Resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        client_socket.close()
        
        if '200' not in response:
            print('Error listing files')
            return
            
        # Mostrando os arquivos disponíveis para download
        lista = json.loads(response.split('\r\n\r\n')[1])
        print('Arquivos disponíveis:')
        for i in range(len(lista)):
            print(f'{i+1}. {lista[i][1]}')
            
        print('\nDigite o número do arquivo que deseja baixar:')
        escolha = int(input().strip()) - 1
        
        if escolha < 0 or escolha >= len(lista):
            print('Selecione uma opção válida')
            time.sleep(3)
            download_file()
        
        print('Baixando arquivo...')
        
        # Preparando request de download
        filename = lista[escolha][1]
        body = json.dumps({'filename': filename})
        headers = (
            f'GET /files/download HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'Content-Length: {len(body)}\r\n'
            f'\r\n'
            f'{body}'
        )
        
        # Enviando request
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.sendall(headers.encode('utf-8'))
        
        # Recebendo a resposta e os pacotes do servidor para download
        response = b''
        while b'\r\n\r\n' not in response:
            response += client_socket.recv(4096)
            
        # Dividindo header e body
        headers = response.split(b'\r\n\r\n')[0].decode('utf-8')
        body = response[response.find(b'\r\n\r\n')+4:]
        
        # Tamanho do conteúdo a ser recebido
        content_length = None
        for line in headers.split('\r\n'):
            if line.startswith('Content-Length:'):
                content_length = int(line.split(': ')[1])
                break
        
        # Recebendo os pacotes de dados do servidor
        while content_length and len(body) < content_length:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            body += chunk
            
        # Salvando o arquivo no diretório de downloads
        downloads_dir = 'downloads'
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
            
        filepath = os.path.join(downloads_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(body)
        
        print(f'\nArquivo salvo em: {filepath}')
        time.sleep(3)
        logged()
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        time.sleep(3)
        logged()
    except Exception as e:
        print(f'Error: {str(e)}')
        time.sleep(3)
        logged()
    finally:
        client_socket.close()
        input('Pressione ENTER para continuar...')
        logged()

def delete_file():
    global USERNAME
    os.system('cls')
    try:
        # Preparando request de listagem de arquivos
        headers = (
            f'GET /files HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.sendall(headers.encode('utf-8'))
        
        # Resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        client_socket.close()
        
        if '200' not in response:
            print('Error listing files')
            return
            
        # Transformando em lista e filtrando os arquivos do usuário logado
        lista = json.loads(response.split('\r\n\r\n')[1])
        lista = list(filter(lambda x: x[3] == USERNAME, lista))
        
        print('Seus arquivos:')
        for i in range(len(lista)):
            print(f'{i+1}. {lista[i][1]}')
            
        print('\nDigite o número do arquivo que deseja apagar:')
        escolha = int(input().strip()) - 1
        
        if escolha < 0 or escolha >= len(lista):
            print('Selecione uma opção válida')
            time.sleep(3)
            delete_file()
        
        print('Apagando arquivo...')
        
        # Preparando request de DELETE
        body = json.dumps({'filename': lista[escolha][1], 'username': USERNAME })
        headers = (
            f'DELETE /files HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        request = headers + body
        
        # Enviando request para o servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.sendall(request.encode('utf-8'))
        
        # Resposta do servidor
        response = client_socket.recv(4096).decode('utf-8')
        if response.find('200') != -1:
            print('Arquivo apagado com sucesso')
            time.sleep(3)
            logged()
        else:
            print('Erro ao apagar arquivo')
            time.sleep(3)
            logged()
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        time.sleep(3)
        logged()
    except Exception as e:
        print(f'Error: {str(e)}')
        time.sleep(3)
        logged()
    finally:
        client_socket.close()
        input('Pressione ENTER para continuar...')
        logged()

def delete_user():
    global USERNAME
    os.system('cls')
    print('Apagando seu usário...')
    try:    
        body = json.dumps({ 'username': USERNAME})
        headers = (
            f'DELETE /user HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        request = headers + body
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.sendall(request.encode('utf-8'))
        
        response = client_socket.recv(4096).decode('utf-8')
        if response.find('200') != -1:
            USERNAME = None
            print('Usuário apagado com sucesso')
            time.sleep(3)
            menu()
        else:
            print("Algo deu errado, tente novamente") 
            time.sleep(3)
            logged()
    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        print('Voltando para o menu...')
        time.sleep(5)
        logged()
    except Exception as e:
        print(f'Error: {str(e)}')
        print('Voltando para o menu...')
        time.sleep(5)
        logged()
    finally:
        client_socket.close()
      
def list_users():
    os.system('cls')
    try:
        headers = (
            f'GET /user HTTP/1.1\r\n'
            f'Host: {HOST}:{SERVER_PORT}\r\n'
            f'\r\n'
        )
        request = headers
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.sendall(request.encode('utf-8'))
        
        response = client_socket.recv(4096).decode('utf-8')

        if response.find('200') == -1:
            print('Error: Could not list files')
            time.sleep(3)
            logged()
        
        lista = json.loads(response.split('\r\n\r\n')[1])
        print('Usuários cadastrados:')
        
        # listando arquivos disponíveis
        for i in range(len(lista)):
            print(f'{i+1}. {lista[i]}')

    except ConnectionRefusedError:
        print('Error: Could not connect to server')
        time.sleep(3)
        logged()
    except Exception as e:
        print(f'Error: {str(e)}')
        time.sleep(3)
        logged()
    finally:
        client_socket.close()
        input('Pressione ENTER para continuar...')
        logged()
    
def logged():
    global USERNAME
    os.system('cls')
    print(f'Olá, {USERNAME}')
    print('1. Listar arquivos existentes')
    print('2. Upload de arquivo')
    print('3. Download de arquivo')
    print('4. Apagar usuário')
    print('5. Apagar arquivo')
    print('6. Listar usuários')
    print('7. Logout')

    
    option = input()
    match option:
        case '1':
            list_files()
        case '2':
            upload_file()
        case '3':
            download_file()
        case '7':
            USERNAME = None
            menu()
        case '4':
            choice = input('Tem certeza que você quer apagar seu usuário? (y/n)')
            if choice == 'y':
                delete_user()
            elif choice == 'n':
                logged()
            else:
                print('Opção inválida')
                time.sleep(2)
                logged()
        case '6':
            list_users()
        case '5':
            delete_file()
        case _:
            print('Selecione uma opção válida')
            time.sleep(2)
            logged()

# Teste inicial para checar se o servidor está online
# Se estiver, continuar com o programa
try:
    headers = (
        f'GET / HTTP/1.1\r\n'
        f'Host: {HOST}:{SERVER_PORT}\r\n'
        f'\r\n'
    )
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(('', CLIENT_PORT))
    client_socket.connect((HOST, SERVER_PORT))
    client_socket.sendall(headers.encode('utf-8'))
    response = client_socket.recv(4096).decode('utf-8')
    if '200' not in response:
        print('Error: Could not connect to server')
        time.sleep(3)
        exit(1)
    menu()
except ConnectionRefusedError:
    print('Error: Could not connect to server')
    time.sleep(3)
    exit(1)
finally:
    client_socket.close()