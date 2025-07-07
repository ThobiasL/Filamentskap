from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index(data1, data2):
    """Render the index page with data from two sensors."""
    return render_template('index.html', data1, data2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)