from flask import Flask, request
import logging
from datetime import datetime
import pytz

app = Flask(__name__)

# Cấu hình múi giờ GMT+7 (Asia/Ho_Chi_Minh)
tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Cấu hình logging với múi giờ GMT+7
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')  # Định dạng thời gian
logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        if not data:
            return {"error": "No JSON data provided"}, 400
        logging.info(f"Dữ liệu nhận được: {data}")
        return {"received": data}, 200
    return {"message": "Hello, World!"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
