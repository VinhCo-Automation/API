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

# Cấu hình kết nối MySQL trên máy tính cục bộ
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),  # Thay đổi thành 'localhost' hoặc '127.0.0.1'
    'port': int(os.getenv('MYSQL_PORT', '3306')),  # Cổng mặc định của MySQL là 3306
    'user': os.getenv('MYSQL_USER', 'root'),  # Thay đổi thành tên người dùng MySQL của bạn
    'password': os.getenv('MYSQL_PASSWORD', '1234'),  # Thay đổi thành mật khẩu MySQL của bạn
    'database': os.getenv('MYSQL_DATABASE', 'my_api'),  # Thay đổi thành tên cơ sở dữ liệu của bạn
}

# Hàm kết nối tới MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        logging.error(f"Lỗi kết nối MySQL: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        if not data:
            return {"error": "Không có dữ liệu JSON được cung cấp"}, 400

        logging.info(f"Dữ liệu nhận được: {data}")

        connection = get_db_connection()
        if connection is None:
            return {"error": "Không thể kết nối đến cơ sở dữ liệu"}, 500

        cursor = None  # Khởi tạo cursor bên ngoài khối try
        try:
            cursor = connection.cursor()
            # Truy vấn INSERT được điều chỉnh để phù hợp với lược đồ bảng của bạn
            query = "INSERT INTO api_1 (ID_DEVICE, DATE, TIME, VALUE_1, VALUE_2) VALUES (%s, %s, %s, %s, %s)"

            # Trích xuất dữ liệu từ JSON. Xử lý các khóa bị thiếu một cách duyên dáng
            id_device = data.get('ID_DEVICE')
            date_str = data.get('DATE')  # Ngày dưới dạng chuỗi (ví dụ: '2024-01-21')
            time_str = data.get('TIME')  # Thời gian dưới dạng chuỗi (ví dụ: '10:30:00')
            value_1 = data.get('VALUE_1')
            value_2 = data.get('VALUE_2')

            # Thực hiện kiểm tra null trước khi chèn
            if any(arg is None for arg in [id_device, date_str, time_str, value_1, value_2]):
                return {"error": "Thiếu các trường bắt buộc"}, 400

            cursor.execute(query, (id_device, date_str, time_str, value_1, value_2)) # Thay đổi số lượng tham số
            connection.commit()
            logging.info(f"Dữ liệu đã được thêm: {id_device}, {date_str}, {time_str}, {value_1}, {value_2}")
            return {"received": data, "message": "Dữ liệu đã được lưu vào MySQL"}, 200

        except Error as e:
            logging.error(f"Lỗi khi thêm dữ liệu: {e}")
            return {"error": "Lỗi khi lưu dữ liệu: " + str(e)}, 500 #Thêm exception để xem lỗi

        finally:
            if cursor: # kiểm tra cursor trước khi đóng
                cursor.close()
            if connection and connection.is_connected():
                connection.close() # Đảm bảo kết nối được đóng

    return {"message": "Hello, World!"}, 200

@app.route('/healthz', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
