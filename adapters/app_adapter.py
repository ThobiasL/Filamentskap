from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Global for siste data
current_data = {
    'temp1': 0,
    'temp2': 0,
    'average_temp': 0,
    'humid1': 0,
    'humid2': 0,
    'average_humid': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(current_data)

@app.route('/update', methods=['POST'])
def update():
    global current_data
    payload = request.get_json()
    # sjekk at alle nøkler finnes
    required = ['temp1','temp2','average_temp','humid1','humid2','average_humid']
    if all(k in payload for k in required):
        current_data = { k: payload[k] for k in required }
        return '', 204
    else:
        return 'Bad payload', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)