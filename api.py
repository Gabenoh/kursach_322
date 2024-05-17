from flask import Flask, jsonify, request, render_template
from db import *


app = Flask(__name__)


# Головна сторінка
@app.route('/')
def home():
    return render_template('main/index.html')


@app.route('/api/get_code', methods=['GET'])
def get_code():
    id, user, clas, code = get_random_deck()
    return jsonify(id=id, user=user, clas=clas, code=code)


@app.route('/api/get_random', methods=['GET'])
def get_random():
    id, user, clas, code = get_random_deck()
    return render_template('get_code/index.html', id=id, user=user, clas=clas, code=code)


@app.route('/api/get_all_code', methods=['GET'])
def get_all_code():
    all_deck_list = get_all_deck()
    print(all_deck_list)
    print(jsonify(all_deck_list))
    return jsonify(all_deck_list)


@app.route('/api/post_code', methods=['POST'])
def post_code():
    user_id = request.json.get('user')
    clas = request.json.get('clas')
    code = request.json.get('code')
    add_deck(user_id, clas, code)
    return jsonify({'message': 'Code added successfully'}), 201


@app.route('/api/delete_code/<int:index>', methods=['DELETE'])
def delete_deck_api(index):
    try:
        delete_deck(index)
        return jsonify({'message': 'Колоду успішно видалено'}), 200
    except KeyError:
        return jsonify({'message': 'Колоду не знайдено'}), 404


# Оновлення існуючого рядка (UPDATE)
@app.route('/update_user/<int:row_id>', methods=['PUT'])
def update_deck_api(row_id):
    clas = request.json.get('clas')
    code = request.json.get('code')
    try:
        update_deck(row_id, clas, code)
        return jsonify({'message': 'User updated successfully'}), 200
    except:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
