from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json  # Lấy dữ liệu JSON từ request POST
        if not data:
            return {"error": "No JSON data provided"}, 400  # Xử lý lỗi nếu không có dữ liệu
        print(data)
        return {"received": data}, 200  # Trả về dữ liệu nhận được
    return {"message": "Hello, World!"}, 200  # Trả về cho GET hoặc các method khác

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
