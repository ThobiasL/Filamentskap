from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Global for siste data
current_data = {'temperature': None, 'humidity': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # Gir siste mottatte data til klienten
    return jsonify(current_data)

@app.route('/update', methods=['POST'])
def update():
    global current_data
    payload = request.get_json()
    if 'average_temp' in payload and 'average_humid' in payload:
        current_data = {
            'temp1': payload['temp1'],
            'temp2': payload['temp2'],
            'average_temp': payload['average_temp'],
            'humid1': payload['humid1'],
            'humid2': payload['humid2'],
            'average_humid': payload['average_humid']
        }
        return '', 204
    else:
        return 'Bad payload', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)