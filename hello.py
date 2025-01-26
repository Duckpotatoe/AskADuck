from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return render_template('AskADuckHome.html')

if __name__ == "__main__":
    app.run(host='localhost', port=80)