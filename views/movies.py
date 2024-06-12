import json
from utils.db import Database
from utils.http_code import HTTPResponseHandler


class Movies:
    def __init__(self, db, handler):
        self.db = db
        self.response_handler = HTTPResponseHandler(handler)

    def list_movies(self, handler, page):
        items_per_page = 3
        page = int(page) - 1  # 将页码从1基转换为0基
        start = items_per_page * page

        # 执行数据库查询
        movies = self.db.query(
            "SELECT id, title FROM movies ORDER BY id LIMIT %s OFFSET %s",
            (items_per_page, start)
        )

        # 将查询结果转换为字典列表
        selected_movies = [{"id": movie[0], "title": movie[1]} for movie in movies]

        self.response_handler.response_json(selected_movies)

    def close(self):
        # 关闭数据库连接
        self.db.close()
