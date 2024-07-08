from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/altas')
def altas():
    return 'Altas page'

if __name__ == '__main__':
    app.run()