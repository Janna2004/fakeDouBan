# Python 课设：影评管理系统（服务端）

## 运行环境
`python 3.10.15`

## 如何部署

1. 复制`config-example.json`为`config.json`，填入自己数据库的信息
2. 控制台运行`pip install -r requirements.txt`
3. 将电影表格数据复制到`data`文件夹下，文件名为`data_movies.xlsx`。 在data下创建`images`文件夹，将电影海报（cover文件夹）图片放入其中，部分文件树如下：
```shell
└─data
   └─img
   │   ├─avartar
   │   └─cover
   ├─data_movies.xlsx
   └─insert_table_data.py
```
4. 执行`data_movies.py`脚本
5. 运行`server.py`，服务运行于`http://127.0.0.1:8000`