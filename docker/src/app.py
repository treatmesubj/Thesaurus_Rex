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
    assert request.method == "POST"
    if request.form["word"] == "":
        return render_template("index.html", error="No word provided")

    return thesr(request_form=request.form)


@app.route("/thesr")
def thesr(request_form):
    thesr_word = Word(request_form["word"])

    word_spelling = thesr_word.spelling

    synonyms_str = ""
    for homonym in thesr_word.thesr_homonyms:
        synonyms_str += f"{{ {homonym['word_class']}: {homonym['definition']} }} == {homonym['synonyms'][:10]}\n"

    # definitions
    #if "define" in request_form.keys():
    #    definitions_str = ""
    #    thesr_word.webster_homonyms = get_defs("word")

    ## etymology
    #if "etymology" in request_form.keys():
    #    etymology_str = ""
    #    thesr_word.etymology = get_etymology("word")

    # antonyms
    if "antonyms" in request_form.keys():
        antonyms_str = ""
        for homonym in thesr_word.thesr_homonyms:
            antonyms_str += f"{{ {homonym['word_class']}: {homonym['definition']} }} =/= {homonym['antonyms'][:10]}\n"

    return render_template(
        "thesr.html",
        word_spelling=word_spelling,
        synonyms_str=synonyms_str,
        # definitions_str=definitions_str,
        # etymology_str=etymology_str,
        antonyms_str=antonyms_str,
    )


if __name__ == "__main__":
    app.run(debug=True)
