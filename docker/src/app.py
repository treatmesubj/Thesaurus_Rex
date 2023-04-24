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
from thesr.thesr import *

# initialise app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index(error=None):
    url_for("static", filename="favicon.css")
    url_for("static", filename="style.css")
    url_for("static", filename="avoid_space.js")
    if request.method == "GET":
        return render_template("index.html")
    else:
        assert request.method == "POST"
        if request.form["word"] == "":
            return render_template("index.html", error="No word provided")

        return thesr(request_form=request.form)


@app.route("/thesr")
def thesr(request_form):
    thesr_word = Word(request_form["word"])
    word_spelling = thesr_word.spelling
    # definitions
    if "define" in request_form.keys():
        thesr_word.webster_homonyms = get_defs("word")
    # etymology
    if "etymology" in request_form.keys():
        thesr_word.etymology = get_etymology("word")
    # antonyms
    if "antonyms" in request_form.keys():
        pass

    return render_template(
        "thesr.html",
        word_spelling=word_spelling,
        # synonyms=synonyms,
        # definitions=definitions,
        # etymology=etymology,
        # antonyms=antonyms,
    )


if __name__ == "__main__":
    app.run(debug=True)
