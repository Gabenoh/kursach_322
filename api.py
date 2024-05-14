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


def add_code(user, clas, code):
    print(user, clas, code)
    id = len(data)
    data.loc[len(data)] = [id, user, clas, code]
    data.to_csv('./data/data.csv', index=False)


@app.route('/api/get_code', methods=['GET'])
def get_code():
    index = rd.randint(0, len(data)-1)
    first_row = data.iloc[index].to_dict()
    print(first_row)
    return jsonify(first_row)


@app.route('/api/post_code', methods=['POST'])
def post_code():
    user_id = request.json.get('user_id')
    clas = request.json.get('class')
    code = request.json.get('code')
    add_code(user_id, clas, code)
    return jsonify({'message': 'Code added successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
