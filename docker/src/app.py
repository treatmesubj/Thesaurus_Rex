from flask import (
    Flask,
    render_template,
    send_file,
    make_response,
    url_for,
    Response,
    redirect,
    request,
)
from thesr import *

# initialise app
app = Flask(__name__)


# decorator for homepage
@app.route("/", methods=['GET', 'POST'])
def index():
    url_for('static', filename='favicon.css')
    url_for('static', filename='style.css')
    url_for('static', filename='avoid_space.js')
    if request.method == 'GET':
        return render_template("index.html")
    else:
        assert request.method == 'POST'
        print(request.form)

        if request.form['word'] != '':
            print(f"word: {request.form['word']}")
            #thesr_word = Word(word)
        if 'define' in request.form.keys():
            print("define")
        if 'etymology' in request.form.keys():
            print("etymology")
        if 'antonyms' in request.form.keys():

            print("antonyms")
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
