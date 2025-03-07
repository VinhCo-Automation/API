from flask import Flask, request, jsonify
import logging
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import pytz

app = Flask(__name__)

# Cấu hình múi giờ GMT+7
tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Cấu hình logging với múi giờ GMT+7
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()

# Cấu hình kết nối MySQL từ Clever Cloud
db_config = {
    'host': os.getenv('MYSQL_ADDON_HOST', 'b3tctusvlvharcpxgk0x-mysql.services.clever-cloud.com'),
    'port': int(os.getenv('MYSQL_ADDON_PORT', '3306')),
    'user': os.getenv('MYSQL_ADDON_USER', 'uutfyaq5terklpid'),
    'password': os.getenv('MYSQL_ADDON_PASSWORD', 'hmFL9JYj9speFoLSuw1d'),  # Thay bằng mật khẩu thực tế
    'database': os.getenv('MYSQL_ADDON_DB', 'b3tctusvlvharcpxgk0x'),
}

# Hàm kết nối tới MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        logging.error(f"Lỗi kết nối MySQL: {e}")
        return None

# API nhận dữ liệu từ thiết bị
@app.route('/', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"error": "Không có dữ liệu JSON"}), 400

    logging.info(f"Dữ liệu nhận được: {data}")

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Không thể kết nối đến MySQL"}), 500

    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO Device_1 (ID_DEVICE, DATE, TIME, VALUE_1, VALUE_2) 
        VALUES (%s, %s, %s, %s, %s)
        """
        # Lấy dữ liệu từ JSON
        id_device = data.get('ID_DEVICE')
        date_str = data.get('DATE')
        time_str = data.get('TIME')
        value_1 = data.get('VALUE_1')
        value_2 = data.get('VALUE_2')

        if any(v is None for v in [id_device, date_str, time_str, value_1, value_2]):
            return jsonify({"error": "Thiếu dữ liệu cần thiết"}), 400

        cursor.execute(query, (id_device, date_str, time_str, value_1, value_2))
        connection.commit()

        logging.info(f"Đã lưu: {id_device}, {date_str}, {time_str}, {value_1}, {value_2}")
        return jsonify({"message": "Dữ liệu đã được lưu"}), 200

    except Error as e:
        logging.error(f"Lỗi khi lưu dữ liệu: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# API lấy dữ liệu từ MySQL
@app.route('/data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Không thể kết nối đến MySQL"}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM api_1 ORDER BY DATE DESC, TIME DESC LIMIT 100")
        rows = cursor.fetchall()
        return jsonify(rows), 200

    except Error as e:
        logging.error(f"Lỗi khi lấy dữ liệu: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# API kiểm tra sức khỏe server
@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
