from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random as rd

# import aiohttp


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/mysql'
# db = SQLAlchemy(app)


data = pd.read_csv('./data/data.csv')


# class Code(db.Model):
#     __tablename__ = 'code'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     clas = db.Column(db.String(255))
#     code = db.Column(db.String(255))


def add_deck(user, clas, code):
    print(user, clas, code)
    new_row = {'id': len(data), 'user': user, 'class': clas, 'code': code}
    data.loc[len(data)+1] = new_row
    data.to_csv('./data/data.csv', index=False)


@app.route('/api/get_code', methods=['GET'])
def get_code():
    index = rd.randint(0, len(data) - 1)
    first_row = data.iloc[index].to_dict()
    first_row['id'] = index
    return jsonify(first_row)


@app.route('/api/post_code', methods=['POST'])
def post_code():
    user_id = request.json.get('user_id')
    clas = request.json.get('class')
    code = request.json.get('code')
    add_deck(user_id, clas, code)
    return jsonify({'message': 'Code added successfully'}), 201


@app.route('/api/delete_code/<int:index>', methods=['DELETE'])
def delete_deck(index):
    try:
        data.drop(index, inplace=True)
        data.to_csv('./data/data.csv', index=False)
        return jsonify({'message': 'Колоду успішно видалено'}), 200
    except KeyError:
        return jsonify({'message': 'Колоду не знайдено'}), 404


if __name__ == '__main__':
    app.run(debug=True)
