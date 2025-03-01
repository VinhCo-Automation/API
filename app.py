from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json  # Lấy dữ liệu JSON từ yêu cầu POST
        return {"received": data}, 200  # Trả về phản hồi
    return "Hello, World!"  # Phản hồi cho GET

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
