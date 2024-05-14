from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Привіт, це мій перший API!'}
    return jsonify(data)


@app.route('/data/', methods=['GET'])
def data_get():
    data = {'message': 'Привіт, це мій перший API!'}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)