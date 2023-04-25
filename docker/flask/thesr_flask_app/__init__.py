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
from waitress import serve
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
    # synonyms
    synonyms_str = ""
    try:
        assert (
            thesr_word.thesr_homonyms is not None and len(thesr_word.thesr_homonyms) > 0
        ), f"no Thesaurus.com homonyms for {word_spelling}"
        for homonym in thesr_word.thesr_homonyms:
            synonyms_str += f"{{ {homonym['word_class']}: {homonym['definition']} }} == {homonym['synonyms'][:10]}\n"
    except Exception as e:
        print(e)
        synonyms_str = "nothin'"

    # definitions
    definitions_str = ""
    if "definitions" in request_form.keys():
        try:
            thesr_word.webster_homonyms = get_defs(word_spelling)
            assert (
                thesr_word.webster_homonyms is not None
                and len(thesr_word.webster_homonyms) > 0
            ), f"no Webster homonyms for {word_spelling}"
            for homonym in thesr_word.webster_homonyms:
                definitions_str += (
                    f"{{ {homonym['word_class']}: {homonym['definition']} }}\n"
                )
        except Exception as e:
            print(e)
            definitions_str = "nothin'"

    # etymology
    etymology_str = ""
    if "etymology" in request_form.keys():
        try:
            thesr_word.etymology = get_etymology(word_spelling)
            assert (
                thesr_word.etymology is not None and len(thesr_word.etymology) > 0
            ), f"no etymonline homonyms for {word_spelling}"
            for homonym in thesr_word.etymology:
                etymology_str += (
                    f"{homonym['word_class']}:\n    {homonym['etym_desc']}\n{'-'*20}\n"
                )
        except Exception as e:
            print(e)
            etymology_str = "nothin'"

    # antonyms
    antonyms_str = ""
    if "antonyms" in request_form.keys():
        try:
            assert (
                thesr_word.thesr_homonyms is not None
                and len(thesr_word.thesr_homonyms) > 0
            ), f"no Thesaurus.com homonyms for {word_spelling}"
            for homonym in thesr_word.thesr_homonyms:
                antonyms_str += f"{{ {homonym['word_class']}: {homonym['definition']} }} =/= {homonym['antonyms'][:10]}\n"
        except Exception as e:
            print(e)
            antonyms_str = "nothin'"

    return render_template(
        "thesr.html",
        word_spelling=word_spelling,
        synonyms_str=synonyms_str,
        definitions_str=definitions_str,
        etymology_str=etymology_str,
        antonyms_str=antonyms_str,
    )


if __name__ == "__main__":
    #app.run(debug=True)
    serve(app, host='0.0.0.0', port=8000, url_scheme='https')
