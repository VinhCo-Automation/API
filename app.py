from flask import Flask, request, jsonify
import logging
from datetime import datetime
import pytz
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Cấu hình múi giờ GMT+7 (Việt Nam)
tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Cấu hình logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()

# Cấu hình MySQL từ Clever Cloud (Bảo mật thông tin bằng biến môi trường)
db_config = {
    'host': os.getenv('MYSQL_ADDON_HOST', 'bq2xyhmvaxjqurdi08ap-mysql.services.clever-cloud.com'),
    'port': int(os.getenv('MYSQL_ADDON_PORT', 3306)),
    'user': os.getenv('MYSQL_ADDON_USER', 'uvacyenejobmkwhw'),
    'password': os.getenv('MYSQL_ADDON_PASSWORD', '######'),  # Cần nhập đúng mật khẩu
    'database': os.getenv('MYSQL_ADDON_DB', 'bq2xyhmvaxjqurdi08ap'),
}

# Hàm kết nối MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        logging.error(f"Lỗi kết nối MySQL: {e}")
        return None

# API nhận dữ liệu từ thiết bị và lưu vào MySQL
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "Không có dữ liệu JSON"}), 400

    logging.info(f"Dữ liệu nhận được: {data}")

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Không thể kết nối đến MySQL"}), 500

    cursor = None
    try:
        cursor = connection.cursor()
        query = "INSERT INTO api_1 (ID_DEVICE, DATE, TIME, VALUE_1, VALUE_2) VALUES (%s, %s, %s, %s, %s)"
        
        id_device = data.get('ID_DEVICE')
        date_str = data.get('DATE')  # Ngày dạng chuỗi 'YYYY-MM-DD'
        time_str = data.get('TIME')  # Giờ dạng chuỗi 'HH:MM:SS'
        value_1 = data.get('VALUE_1')
        value_2 = data.get('VALUE_2')

        if any(arg is None for arg in [id_device, date_str, time_str, value_1, value_2]):
            return jsonify({"error": "Thiếu dữ liệu"}), 400

        cursor.execute(query, (id_device, date_str, time_str, value_1, value_2))
        connection.commit()
        logging.info(f"Lưu vào MySQL: {id_device}, {date_str}, {time_str}, {value_1}, {value_2}")
        return jsonify({"message": "Dữ liệu đã được lưu"}), 200

    except Error as e:
        logging.error(f"Lỗi khi lưu dữ liệu: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# API kiểm tra server
@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "Server hoạt động tốt"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
