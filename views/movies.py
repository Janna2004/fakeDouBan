import json
from utils.db import Database
from utils.http_code import HTTPResponseHandler


class Movies:
    def __init__(self, db, handler):
        self.db = db
        self.response_handler = HTTPResponseHandler(handler)

    def list_movies(self, page):
        items_per_page = 12
        page = int(page) - 1  # 将页码从1基转换为0基
        start = items_per_page * page

        # 执行数据库查询
        movies = self.db.fetch(
            "SELECT * FROM movies ORDER BY id LIMIT %s OFFSET %s",
            (items_per_page, start)
        )

        # 将查询结果转换为字典列表
        selected_movies = [{
            "rank": movie[1],
            "name": movie[2],
            "director": movie[3],
            "writer": movie[4],
            "starring": movie[5],
            "type": movie[6],
            "country": movie[7],
            "language": movie[8],
            "rating": movie[12],
            "note": movie[19],
            "releaseDate": movie[9],
            "runTime": movie[10],
            "imdbHref": movie[11],
            "commentsUser": movie[13],
            "starRatio": [movie[14], movie[15], movie[16], movie[17], movie[18]],
            "coverUrl": movie[21],
        } for movie in movies]
        data = {
            "page": page + 1,
            "movies": selected_movies
        }
        self.response_handler.response_json(data)

    def close(self):
        # 关闭数据库连接
        self.db.close()
