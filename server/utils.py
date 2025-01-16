# construtor de mensagens HTTP
def http_response(status_code, body, content_type='text/plain'):
    status_messages = {200: 'OK', 201: 'Created', 400: 'Bad Request', 
                      404: 'Not Found', 500: 'Internal Server Error'}
    
    headers = [
        f'HTTP/1.1 {status_code} {status_messages[status_code]}',
        'Access-Control-Allow-Origin: *',
        'Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers: Content-Type',
        'Access-Control-Allow-Credentials: true',
        f'Content-Type: {content_type}'
    ]
    
    return f'{chr(10).join(headers)}\r\n\r\n{body}'.encode('utf-8')