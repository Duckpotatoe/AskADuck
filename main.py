from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def indexPage():
    return render_template('AskADuckHome.html')

@app.route('/about', methods=['GET'])
def aboutPage():
    return render_template("AskADuckAbout.html")

if __name__ == "__main__":
    app.run(host='localhost', port=80)