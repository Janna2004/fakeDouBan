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

    def handle_request(self, method):
        parsed_path = urllib.parse.urlparse(self.path)
        path_components = parsed_path.path.strip('/').split('/')

        if method == 'GET':
            try:
                if path_components[0] == "list" and len(path_components) == 2:
                    page = int(path_components[1])
                    self.movies.list_movies(page)
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
                else:
                    http_code.HTTPResponseHandler(self).not_found()
            except json.JSONDecodeError:
                http_code.HTTPResponseHandler(self).server_error()


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting httpd server...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
