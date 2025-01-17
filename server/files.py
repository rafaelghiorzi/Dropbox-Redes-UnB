from utils import http_response
import json
import sqlite3
import os
import mimetypes

# rotas de arquivos
UPLOAD_DIR = 'uploads'

def list_files():
    try:
        connection = sqlite3.connect('server.db')
        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM files')
        files = cursor.fetchall()
        connection.close()
        
        return http_response(200, json.dumps(files))
    except Exception as e:
        return http_response(500, f'Error: {e}')

def upload(headers, body, client_socket):
    try:
        # Parse headers
        header_lines = headers.split('\r\n')
        content_length = None
        boundary = None
        
        for line in header_lines:
            if 'Content-Length: ' in line:
                content_length = int(line.split('Content-Length: ')[1])
            elif 'Content-Type: ' in line and 'boundary=' in line:
                boundary = line.split('boundary=')[1].strip()
        
        if not content_length or not boundary:
            return http_response(400, "Missing required headers")
        
        # Recebendo tamanho do arquivo
        received_length = len(body)
        
        # Lendo o restante do arquivo
        while received_length < content_length:
            chunk = client_socket.recv(min(8192, content_length - received_length))
            if not chunk:
                break
            body += chunk
            received_length += len(chunk)
            
        # Dividir o corpo da requisição em partes
        boundary = f'--{boundary}'
        parts = body.split(boundary.encode('utf-8'))
        
        # Processando cada parte da requisição, metadata e arquivo
        metadata = None
        file_content = None
        
        for part in parts:
            if b'name="metadata"' in part:
                meta_start = part.find(b'{')
                meta_end = part.find(b'}') + 1
                if meta_start != -1 and meta_end != -1:
                    metadata = json.loads(part[meta_start:meta_end])
            
            elif b'name="file"' in part:
                content_start = part.find(b'\r\n\r\n') + 4
                if content_start > 0:
                    file_content = part[content_start:]
                    if file_content.endswith(b'\r\n'):
                        file_content = file_content[:-2]
        
        if not metadata or not file_content:
            return http_response(400, "Missing metadata or file content")
            
        # Salvando arquivo na pasta de uploads
        filepath = os.path.join(UPLOAD_DIR, metadata['name'])
        with open(filepath, 'wb') as f:
            f.write(file_content)
            
        # Salvando metadados no banco de dados
        conn = sqlite3.connect('server.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO files (name, path, user_username) VALUES (?, ?, ?)',
            (metadata['name'], metadata['name'], metadata['user_username'])
        )
        conn.commit()
        conn.close()
        
        return http_response(201, 'File uploaded successfully')
        
    except Exception as e:
        print(f'Upload error: {e}')
        return http_response(500, str(e))

def download(headers, body):
    try:
        # Parse JSON
        request_data = body.decode('utf-8')
        data = json.loads(request_data)
        filename = data.get('filename')
        
        if not filename:
            return http_response(400, 'Filename not provided')
            
        # Checando existência
        filepath = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(filepath):
            return http_response(404, 'File not found')
            
        # Lendo o arquivo
        with open(filepath, 'rb') as f:
            file_content = f.read()
            
        # Criando cabeçalho HTTP
        content_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        headers = (
            f' 200 OK\r\n'
            f'Content-Type: {content_type}\r\n' 
            f'Content-Disposition: attachment; filename={filename}\r\n'
            f'Content-Length: {len(file_content)}\r\n'
            f'\r\n'
        ).encode('utf-8')
        
        # Devolvendo os headers e o conteúdo do arquivo
        return headers + file_content
        
    except Exception as e:
        print(f'Download error: {e}')
        return http_response(500, str(e))

def delete_file(headers, body):
    try:
        # Parse JSON
        request_data = body.decode('utf-8')
        data = json.loads(request_data)
        filename = data.get('filename')
        username = data.get('username')
        
        if not filename:
            return http_response(400, 'Filename not provided')
        if not username:
            return http_response(400, 'Username not provided')    
        
        # Checando existência
        filepath = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(filepath):
            return http_response(404, 'File not found')
            
        # DELETE do arquivo
        os.remove(filepath)
        
        # DELETE os metadados do banco de dados
        conn = sqlite3.connect('server.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files WHERE name = ? AND user_username = ?', (filename, username))
        conn.commit()
        conn.close()
        
        return http_response(200, 'File deleted successfully')
        
    except Exception as e:
        print(f'Delete error: {e}')
        return http_response(500, str(e))
    