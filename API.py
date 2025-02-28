from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Dữ liệu mẫu
data_store = {
    "users": [
        {"id": 1, "name": "Nguyen Van A", "age": 25},
        {"id": 2, "name": "Tran Thi B", "age": 30}
    ]
}

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(data_store)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in data_store["users"] if user["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    new_id = max(user["id"] for user in data_store["users"]) + 1
    new_user["id"] = new_id
    data_store["users"].append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    # Lấy port từ biến môi trường (Render cung cấp)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
