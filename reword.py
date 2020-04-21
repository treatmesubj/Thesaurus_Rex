import requests
from requests_html import HTML
import re
import json
import sys
import random
from nltk import pos_tag, word_tokenize
import string
from nltk.tokenize import TweetTokenizer
from MontyLingua import MontyNLGenerator
import inflect


"""
This is a funny language processing project. It attempts to re-word a sentence
with synonyms using proper conjugations and such. 
"""


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
    'VBN': 'adj.',
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

verb_types = {
    'VB': 'verb',
    'VBD': 'verb',
    'VBG': 'verb',
    'VBN': 'adj.',
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
}

ignored_words = ("is", "and", "be")


tknzr = TweetTokenizer()
monty = MontyNLGenerator.MontyNLGenerator()
plur = inflect.engine()


sentence = "I should probably lift soon. I've been obsessed with coding this all day. I am very satisfied, though."
while True:
    sentence = input("sentence: ")
    word_tokens = pos_tag(tknzr.tokenize(sentence))
    print(f"{sentence=}")
    # print(f"{word_tokens=}")

    new_word_tokens = []


    for word_token in word_tokens:
        tag = word_token[1]
        word = word_token[0]

        if tag in tags and word not in ignored_words:

            try:
                
                thesr_word = Word(word)
                for homonym in thesr_word.homonyms:
                    if homonym['word_class'] == tags[tag]:

                        replacement = homonym['synonyms'][random.randint(0, len(homonym['synonyms'])-1)]
                        replacement_tagged = pos_tag(tknzr.tokenize(replacement))
                        
                        # check for conjugation
                        if tag in verb_types:
                            for rep_index, rep_word_token in enumerate(replacement_tagged):
                                if 'V' in rep_word_token[1] or 'NN' in rep_word_token[1]:
                                    try:
                                        conjugated = monty.conjugate_verb(rep_word_token[0], tag)
                                        replacement_tagged[rep_index] = (conjugated, tag)
                                        for rep_tag in replacement_tagged:
                                            new_word_tokens.append(rep_tag)
                                        break
                                    except Exception as e:
                                        # print(e)
                                        new_word_tokens.append(word_token)
                            break

                        # check for plural
                        if tag == 'NNS':
                            for rep_index, rep_word_token in enumerate(replacement_tagged):
                                if 'NN' in rep_word_token[1]:
                                    try:
                                        plural = plur.plural(rep_word_token[0])
                                        replacement_tagged[rep_index] = (plural, tag)
                                        for rep_tag in replacement_tagged:
                                            new_word_tokens.append(rep_tag)
                                        break
                                    except Exception as e:
                                        # print(e)
                                        new_word_tokens.append(word_token)
                            break

                        else:
                            # no need to conjugate
                            for rep_tag in replacement_tagged:
                                new_word_tokens.append(rep_tag)
                            break

                        # check for capitalization
                        # if word.spelling == word.spelling.capitalize():
                        #     replacement = replacement[0][1].capitalize()

                    else:  # wrong homonym
                        pass
                else:
                    new_word_tokens.append(word_token)

            except Exception as e:
                # print(e)
                new_word_tokens.append(word_token)
                pass

        else:
            new_word_tokens.append(word_token)

    # print(f"{new_word_tokens=}")
    new_sentence = "".join([" "+token[0] if not token[0].startswith("'") and token[0] not in string.punctuation else token[0] for token in new_word_tokens]).strip()
    print(f"{new_sentence=}", end='\n\n')

