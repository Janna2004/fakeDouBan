# 运行数据插入脚本
echo "Running data insertion script..."
python data/insert_table_data.py

# 运行服务器
echo "Starting server..."
exec python server.py
