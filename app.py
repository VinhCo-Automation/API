from flask import Flask, request
import logging
from datetime import datetime
import pytz
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Cấu hình múi giờ GMT+7
tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Cấu hình logging với múi giờ GMT+7
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()

# Cấu hình kết nối MySQL từ biến môi trường
db_config = {
    'host': os.getenv('MYSQL_HOST', 'mysql-2f0079d3-covo488-2c24.1.aivencloud.com'),
    'port': int(os.getenv('MYSQL_PORT', '24173')),
    'user': os.getenv('MYSQL_USER', 'avnadmin'),
    'password': os.getenv('MYSQL_PASSWORD', 'AVNS_LtPth-518YorMfZzh5H'),
    'database': os.getenv('MYSQL_DATABASE', 'defaultdb'),
    'ssl_ca': os.getenv('MYSQL_SSL_CA', None)  # Lấy CA certificate từ biến môi trường
}

# Hàm kết nối tới MySQL
def get_db_connection():
    try:
        # Nếu ssl_ca là chuỗi (nội dung certificate), tạo file tạm thời
        ssl_ca_path = None
        if db_config['ssl_ca'] and isinstance(db_config['ssl_ca'], str):
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pem') as f:
                f.write(db_config['ssl_ca'])
                ssl_ca_path = f.name
            db_config['ssl_ca'] = ssl_ca_path

        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        logging.error(f"Lỗi kết nối MySQL: {e}")
        return None
    finally:
        # Xóa file tạm thời nếu tạo
        if ssl_ca_path and os.path.exists(ssl_ca_path):
            import os
            os.unlink(ssl_ca_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        if not data:
            return {"error": "No JSON data provided"}, 400
        
        logging.info(f"Dữ liệu nhận được: {data}")
        
        connection = get_db_connection()
        if connection is None:
            return {"error": "Không thể kết nối đến cơ sở dữ liệu"}, 500
        
        try:
            cursor = connection.cursor()
            # Giả sử bảng 'items' có các cột: name và value
            query = "INSERT INTO items (name, value) VALUES (%s, %s)"
            name = data.get('name')
            value = data.get('value')
            cursor.execute(query, (name, value))
            connection.commit()
            logging.info(f"Dữ liệu đã được thêm: {name}, {value}")
            return {"received": data, "message": "Dữ liệu đã được lưu vào MySQL"}, 200
        
        except Error as e:
            logging.error(f"Lỗi khi thêm dữ liệu: {e}")
            return {"error": "Lỗi khi lưu dữ liệu"}, 500
        
        finally:
            cursor.close()
            connection.close()
    
    return {"message": "Hello, World!"}, 200

@app.route('/healthz', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
