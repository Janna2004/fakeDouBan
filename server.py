from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import views.movies
import views.users as users
import utils.db
from utils import http_code
import json


def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        config = load_config('config.json')
        db_config = config['database']
        self.db = utils.db.Database(dbname=db_config['dbname'],
                           user=db_config['user'],
                           password=db_config['password'],
                           host=db_config['host'])
        self.movies = views.movies.Movies(self.db, self)
        self.users = views.users.Users(self.db, self)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def do_PUT(self):
        self.handle_request('PUT')

    def handle_request(self, method):
        parsed_path = urllib.parse.urlparse(self.path)
        path_components = parsed_path.path.strip('/').split('/')
        # 使用urllib解析查询参数，得到一个字典
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if method == 'GET':
            try:
                if path_components[0] == "list" and len(path_components) == 2:
                    page = int(path_components[1])
                    self.movies.list_movies(page)
                elif path_components[0] == "movie" and len(path_components) == 2:
                    if path_components[1] == "search":
                        self.movies.search_movies(query_params)
                elif path_components[0] == "user" and len(path_components) == 2:
                    if path_components[1] == "info":
                        self.users.user_info(query_params)
                    elif path_components[1] == "all":
                        self.users.all_user()
                else:
                    http_code.HTTPResponseHandler(self).not_found()
            except json.JSONDecodeError:
                http_code.HTTPResponseHandler(self).server_error()

        elif method == 'POST':
            try:
                content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(post_data)
                if path_components[0] == "user":
                    if path_components[1] == "login":
                        self.users.login(data)
                    elif path_components[1] == "signup":
                        self.users.signup(data)
                    elif path_components[1] == "modify":
                        if path_components[2] == "name":
                            self.users.modify_name(data)
                        elif path_components[2] == "pwd":
                            self.users.modify_pwd(data)
                else:
                    http_code.HTTPResponseHandler(self).not_found()
            except json.JSONDecodeError:
                http_code.HTTPResponseHandler(self).server_error()

        elif method == 'DELETE':
            try:
                if path_components[0] == "user" and len(path_components) == 2:
                    if path_components[1] == "delete":
                        self.users.delete_user(query_params)
            except:
                http_code.HTTPResponseHandler(self).server_error()

        elif method == 'PUT':
            try:
                if path_components[0] == "user" and len(path_components) == 2:
                    if path_components[1] == "admin":
                        self.users.add_admin(query_params)
            except:
                http_code.HTTPResponseHandler(self).server_error()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd server...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
