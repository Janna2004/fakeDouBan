import json

class HTTPResponseHandler:
    def __init__(self, handler):
        self.handler = handler

    def send(self, status_code, content_type, content):
        self.handler.send_response(status_code)
        self.handler.send_header('Content-type', content_type)
        self.handler.end_headers()
        self.handler.wfile.write(content.encode() if not isinstance(content, bytes) else content)

    def not_found(self):
        self.send(404, 'text/html', '未找到路由')

    def server_error(self, content='服务器内部错误'):
        self.send(500, 'text/html', content)

    def parse_error(self, content='请求解析错误'):
        self.send(400, 'text/html', content)

    def ok(self, content, content_type='text/html'):
        self.send(200, content_type, content)

    def response_json(self, data):
        json_content = json.dumps(data)
        self.ok(json_content, content_type='application/json')
