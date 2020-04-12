import requests
from requests_html import HTML
import re
import json
import sys
import random
from nltk import pos_tag, word_tokenize
import string


def get_random_word():
    session = requests.session()
    html = HTML(html=session.get("https://www.merriam-webster.com/word-of-the-day/calendar").text)
    word_elems = html.find("div.more-words-of-day-container ul.more-wod-items li h2 a")
    words = [word_elem.text for word_elem in word_elems]
    random_word = words[random.randint(0, len(words))]
    return random_word


def get_syns(word):

    session = requests.session()
    url = f"http://www.thesaurus.com/browse/{word}"
    html = session.get(url, headers={"user-agent": "Mozilla/5.0"}).text
    script = re.search(r'<script>window\.INITIAL_STATE = (.+);</script>', html).group(1)

    while True:
        try:
            j = json.loads(script)
            break
        except json.decoder.JSONDecodeError:
            bitches = [u.start() for u in re.finditer(":undefined", script)]
            if len(bitches) > 0:
                script = script.replace(":undefined", ":\"undefined\"")
            bitches = [u.start() for u in re.finditer(":null", script)]
            if len(bitches) > 0:
                script = script.replace(":null", ":\"null\"")
        except Exception:
            print("Not today!")
            raise

    try:
        posTabs = j['searchData']['tunaApiData']['posTabs']
    except TypeError:
        # print(f"is {word} a word?")
        return

    homonyms = []

    for tab in posTabs:
        # print(f"<{tab['pos']}: {tab['definition']}> ~~~~~~~~~ {[s['term'] for s in tab['synonyms'][:10]]}")
        homonyms.append({
            'word_class': tab['pos'],
            'definition': tab['definition'],
            'synonyms': [s['term'] for s in tab['synonyms']]
            })

    return(homonyms)


class Word:
    def __init__(self, word):
        self.spelling = word
        self.homonyms = get_syns(self.spelling)

    def show_syns(self):
        for homonym in self.homonyms:
            print(f"<{homonym['word_class']}: {homonym['definition']}> ~~~~~~~~~ {homonym['synonyms'][:10]}")


tags = {
    'CC': 'conj.',
    'JJ': 'adj.',
    'JJR': 'adj.',
    'JJS': 'adj.',
    'NN': 'noun',
    'NNS': 'noun',
    'PP': 'noun',
    'PPZ': 'adj.',
    'RB': 'adv.',
    'RBR': 'adv.',
    'RBS': 'best',
    'VB': 'verb',
    'VBD': 'verb',
    'VBG': 'verb',
    'VBN': 'verb',
    'VBP': 'verb',
    'VBZ': 'verb',
    'VH': 'verb',
    'VHD': 'verb',
    'VHG': 'verb',
    'VHN': 'verb',
    'VHP': 'verb',
    'VHZ': 'verb',
    'VV': 'verb',
    'VVD': 'verb',
    'VVG': 'verb',
    'VVN': 'verb',
    'VVP': 'verb',
    'VVZ': 'verb',
    'WDT': 'conj',
    'WP': 'pron.',
    'WRB': 'adv.'
    }

ignored_words = ("is")

sentence = "I wonder what the weather will be like tomorrow. I hope the sky is blue."
tokens = pos_tag(word_tokenize(sentence))
print(sentence)
# print(tokens)

for index, token in enumerate(tokens):
    if token[1] in tags and token[0] not in ignored_words:
        try:
            # print(token[0])
            word = Word(token[0])
            for homonym in word.homonyms:
                if homonym['word_class'] == tags[token[1]]:
                    # print(homonym['synonyms'][0])
                    tokens[index] = (homonym['synonyms'][0], token[1])
                    break
            # print("~~~~~~~~~~~~~~~~")
        except Exception:
            pass

new_sentence = "".join([" "+token[0] if not token[0].startswith("'") and token[0] not in string.punctuation else token[0] for token in tokens]).strip()
print(new_sentence)