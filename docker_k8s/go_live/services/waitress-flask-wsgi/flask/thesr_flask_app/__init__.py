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

# from waitress import serve
import os
from thesr.thesr import thesaurus, dictionary

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
    word_spelling = request_form["word"]

    synonyms_antonyms_str = ""
    # TODO: handle spellcheck response
    try:
        sanjay = thesaurus(word=word_spelling, apikey=os.getenv("websterthesrapikey"))
        for homograph in sanjay or []:
            synonyms_antonyms_str += f"({homograph['fl']}) {homograph['def']}"
            if len(homograph["syns"]) >= len(homograph["sims"]):
                synonyms_antonyms_str += f"\n\tsynonyms: {homograph['syns']}"
            else:
                synonyms_antonyms_str += f"\n\tnear-synonyms: {homograph['sims']}"

            if len(homograph["ants"]) > 0 or len(homograph["opps"]) > 0:
                if len(homograph["ants"]) >= len(homograph["opps"]):
                    synonyms_antonyms_str += f"\n\tantonyms: {homograph['ants']}"
                else:
                    synonyms_antonyms_str += f"\n\tnear-antonyms: {homograph['opps']}"
            synonyms_antonyms_str += "\n\n"
    except Exception as e:
        print(e)
        synonyms_antonyms_str = "nothin'"

    # definitions
    definitions_etymology_str = ""
    if "definitions" in request_form.keys():
        try:
            sanjay = dictionary(word=word_spelling, apikey=os.getenv("websterdictapikey"))
            for homograph in sanjay or []:
                definitions_etymology_str += f"({homograph['fl']}) {homograph['def'][0]}"
                for defi in homograph["def"][1:]:
                    definitions_etymology_str += f"\n\t{defi}"

                if homograph["etymology"][0] is not None:
                    definitions_etymology_str += f"\netymology:\n\t{homograph['etymology'][0]}"
                    for ety in homograph["etymology"][1:]:
                        definitions_etymology_str += f"\n\t{ety}"
                definitions_etymology_str += "\n\n"
        except Exception as e:
            print(e)
            definitions_etymology_str = "nothin'"


    return render_template(
        "thesr.html",
        word_spelling=word_spelling,
        synonyms_antonyms_str=synonyms_antonyms_str,
        definitions_etymology_str=definitions_etymology_str,
    )


if __name__ == "__main__":
    app.run()
    # serve(app, host='0.0.0.0', port=8000, url_scheme='https')
