import socket
import os
import sqlite3
from  urllib.parse import unquote
import signal
from user import register, login, delete_user, list_users
from files import list_files, upload, download, delete_file
from utils import http_response

# configuração do servidor
HOST = '0.0.0.0'
PORT = 8080
UPLOAD_DIR = 'uploads'

# inicialização do banco de dados
def init_db():
    connection = sqlite3.connect('server.db')
    cursor = connection.cursor() 
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Tabela de arquivos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            user_username TEXT NOT NULL,
            FOREIGN KEY(user_username) REFERENCES user(username) ON DELETE CASCADE
        )
    ''')
    
    connection.commit()
    connection.close()

# processamento de requisições HTTP
def handle_request(client_socket):
    try:
        # Lendo os dados da requisição em chunks em binário
        request_data = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            request_data += chunk
            if b'\r\n\r\n' in request_data and len(chunk) < 4096:
                break
            
        print(f'\n\nConnection incoming from {client_socket.getpeername()}')
        
        # Dividindo cabeçalhos e corpo da requisição
        headers_end = request_data.find(b'\r\n\r\n')
        headers = request_data[:headers_end].decode('utf-8')
        body = request_data[headers_end + 4:]
        
        # Dividindo a primeira linha dos cabeçalhos
        first_line = headers.split('\r\n')[0]
        method, path, _ = first_line.split(' ')
        path = unquote(path)
        
        # Roteamento de requisições que tem bytes envolvidos
        if method == 'POST' and path == '/files/upload':
            response = upload(headers, body, client_socket)
        elif method == 'GET' and path == '/files/download':
            response = download(headers, body)
        elif method == 'DELETE' and path == '/files':
            response = delete_file(headers, body)
        else:
            # Roteamento de requisições plain text
            request = request_data.decode('utf-8')
            if method == 'GET' and path == '/':
                response = http_response(200, 'Server running')
            elif method == 'POST' and path == '/user/register':
                response = register(request)
            elif method == 'POST' and path == '/user/login':
                response = login(request)
            elif method == 'GET' and path == '/user':
                response = list_users()
            elif method == 'DELETE' and path == '/user':
                response = delete_user(request)
            elif method == 'GET' and path == '/files':
                response = list_files()
            else:
                response = http_response(404, 'Not Found')
        
        client_socket.sendall(response)
        print(request, '\n\n\n\n', response)
        
    except Exception as e:
        print(f'Error handling request: {e}')
        response = http_response(500, str(e))
        client_socket.sendall(response)
    finally:
        client_socket.close()

    
def start_server():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    init_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    
    os.system('cls')
    print(f'Servidor rodando em {HOST}:{PORT}')
    
    def signal_handler(sig, frame):
        print('Encerrando servidor...')
        server_socket.close()
        exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        client_socket, _ = server_socket.accept()
        handle_request(client_socket)
        
if __name__ == '__main__':
    start_server()
    
