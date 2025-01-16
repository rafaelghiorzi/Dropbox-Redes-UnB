from utils import http_response
import json
import sqlite3


# rotas de usuário
def register(request):
    try:
        headers, body = request.split('\r\n\r\n', 1)
        
        # parse do corpo da requisição
        data = json.loads(body)
        
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return http_response(400, 'Bad Request: Missing username or password')
        
        # criação do usuário
        connection = sqlite3.connect('server.db')
        cursor = connection.cursor()
        
        cursor.execute('INSERT INTO user (username, password) VALUES (?, ?)', (data['username'], data['password']))
        connection.commit()
        connection.close()
        
        return http_response(201, username)
    except Exception as e:
        return http_response(500, f'Error: {e}')
    
def login(request):
    try:
        headers, body = request.split('\r\n\r\n', 1)
        
        # parse do corpo da requisição
        data = json.loads(body)
        # checagem do corpo da requisição
        # tem que conter apenas dois elementos: {'username': '...', 'password': '...'}
        if not isinstance(data, dict) or len(data) != 2:
            return http_response(400, 'Bad Request')
        # checar se é tudo string
        if not all(isinstance(value, str) for value in data.values()):
            return http_response(400, 'Bad Request')
        
        # autenticação do usuário
        connection = sqlite3.connect('server.db')
        cursor = connection.cursor()
        
        cursor.execute('SELECT * FROM user WHERE username = ? AND password = ?', (data['username'], data['password']))
        user = cursor.fetchone()
        connection.close()
        
        if user:
            return http_response(200, data['username'])
        return http_response(401, 'Unauthorized')
    except Exception as e:
        return http_response(500, f'Error: {e}')
    
def delete_user(request):
    try:
        headers, body = request.split('\r\n\r\n', 1)
        
        # parse do corpo da requisição
        data = json.loads(body)
        # checagem do corpo da requisição
        # tem que conter apenas um elemento: {'username': '...'}
        if not isinstance(data, dict) or len(data) != 1:
            return http_response(400, 'Bad Request')
        # checar se é tudo string
        if not all(isinstance(value, str) for value in data.values()):
            return http_response(400, 'Bad Request')
        
        # remoção do usuário
        connection = sqlite3.connect('server.db')
        cursor = connection.cursor()
        
        cursor.execute('DELETE FROM user WHERE username = ?', (data['username'],))
        connection.commit()
        connection.close()
        return http_response(200, 'OK')
    except Exception as e:
        return http_response(500, f'Error: {e}')
    
def list_users():
    try:
        connection = sqlite3.connect('server.db')
        cursor = connection.cursor()
        
        cursor.execute('SELECT username FROM user')
        users = cursor.fetchall()
        connection.close()
        
        users = [user[0] for user in users]
        return http_response(200, json.dumps(users))
    except Exception as e:
        return http_response(500, f'Error: {e}')
    
    
if __name__ == '__main__':
    print(list_users())