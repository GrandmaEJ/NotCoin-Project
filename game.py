from flask import Flask, render_template, request, jsonify
import json

web_app = Flask(__name__)

def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file)

data = load_data()

@web_app.route('/play/<user_id>', methods=['GET'])
def play_game(user_id):
    return render_template('game.html', user_id=user_id)

@web_app.route('/api/update', methods=['POST'])
def update_game():
    data_request = request.json
    user_id = str(data_request['user_id'])
    action = data_request['action']
    if action == 'tap':
        data[user_id]['coins'] += 1
        save_data(data)
        return jsonify(status="success", coins=data[user_id]['coins'])
    return jsonify(status="error")
    