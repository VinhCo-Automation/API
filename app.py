from flask import Flask, request
#import logging

# Cấu hình logging
#logging.basicConfig(
#    level=logging.INFO,  # Mức log (INFO, DEBUG, ERROR, v.v.)
#    format='%(asctime)s - %(levelname)s - %(message)s'  # Định dạng log
#)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json  # Lấy dữ liệu JSON từ yêu cầu POST
#        logging.info(f"Dữ liệu nhận được: {data}")  # Ghi log với logging
        print(data)
        return {"received": data}, 200
#    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
