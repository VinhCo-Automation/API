from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        if not data:
            return {"error": "No JSON data provided"}, 400
        print(json.dumps(data, indent=4, ensure_ascii=False))  # In đẹp hơn
        return {"received": data}, 200
    return {"message": "Hello, World!"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
