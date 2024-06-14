from utils.http_code import HTTPResponseHandler
import threading


class Movies:
    def __init__(self, db, handler):
        self.db = db
        self.response_handler = HTTPResponseHandler(handler)
        self.lock = threading.Lock()

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

    def search_movies(self, query_params):
        # 假设 type 必须是以下几种之一
        valid_types = {'name', 'director', 'starring', 'type', 'country'}
        type = query_params.get('type', [None])[0]
        text = query_params.get('text', [None])[0]

        if type in valid_types and text is not None:
            query_name = f'movie_{type}'  # 构建列名
            query_text = f'%{text}%'  # 构建 LIKE 查询的参数

            sql = f"SELECT * FROM movies WHERE {query_name} LIKE %s ORDER BY id"  # 安全地构建 SQL 语句
            movies = self.db.fetch(sql, (query_text,))  # 执行查询
            # 处理 movies 结果
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
                "movies": selected_movies
            }

            self.response_handler.response_json(data)

        else:
            self.response_handler.parse_error('Invalid query parameters')
