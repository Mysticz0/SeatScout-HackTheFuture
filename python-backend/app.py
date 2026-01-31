from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Running Successfully!'})

@app.route('/check-all-spaces')
def check_all_spaces():
    spaces = {
        'A1': {'status': 'free', 'person count': 0},
        'A2': {'status': 'taken', 'person count': 1},
        'A3': {'status': 'taken', 'person count': 3}
    }
    return jsonify(spaces)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
