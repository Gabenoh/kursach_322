from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import aiohttp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:60199@localhost/mysql'
db = SQLAlchemy(app)


class Code(db.Model):
    __tablename__ = 'code'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    clas = db.Column(db.String(255))
    code = db.Column(db.String(255))


async def add_code(user_id, clas, code):
    url = 'http://localhost:5000/api/codes'
    data = {'user_id': user_id, 'cals': clas, 'code': code}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()


@app.route('/api/get_code', methods=['GET'])
def get_code():
    code = Code.query.first()  # Припустимо, що у вас є модель Code
    if code:
        return jsonify({'code': code.code})
    else:
        return jsonify({'code': None})


if __name__ == '__main__':
    app.run(debug=True)
