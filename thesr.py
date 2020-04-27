import requests
from requests_html import HTML
import re
import json
import sys
import random


def get_random_word():
    session = requests.session()
    html = HTML(html=session.get("https://www.merriam-webster.com/word-of-the-day/calendar").text)
    word_elems = html.find("div.more-words-of-day-container ul.more-wod-items li h2 a")
    words = [word_elem.text for word_elem in word_elems]
    random_word = words[random.randint(0, len(words))]
    return random_word


def get_defs(word):
    session = requests.session()
    html = HTML(html=session.get(f"https://www.merriam-webster.com/dictionary/{word}").text)
    dict_entry_elems = html.find("div[id*='dictionary-entry']")
    word_class_elems = html.find("div.row.entry-header a.important-blue-link")[:len(dict_entry_elems)]
    zipped_elems = zip(dict_entry_elems, word_class_elems)

    homonyms = []

    try:
        for dict_entry_elem, word_class_elem in zipped_elems:
            definition = dict_entry_elem.find("span.dtText", first=True).text[2:]
            word_class = word_class_elem.text
            homonyms.append({
                'definition': definition,
                'word_class': word_class
                })
        return(homonyms)
    except Exception:
        return


def get_syns(word):
    session = requests.session()
    print(f"[{word}!]", end="\n\n")

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
            return

    try:
        posTabs = j['searchData']['tunaApiData']['posTabs']
    except TypeError:
        return

    homonyms = []

    for tab in posTabs:
        homonyms.append({
            'word_class': tab['pos'],
            'definition': tab['definition'],
            'synonyms': [s['term'] for s in tab['synonyms']]
            })

    return(homonyms)


class Word:
    def __init__(self, word):
        self.spelling = word
        self.thesr_homonyms = get_syns(self.spelling)
        if not getattr(self, "thesr_homonyms", None):
            self.webster_homonyms = get_defs(self.spelling)

    def show_syns(self):
        if getattr(self, "thesr_homonyms", None):
            for homonym in self.thesr_homonyms:
                print(f"<{homonym['word_class']}: {homonym['definition']}> ~~~~~~~~~ {homonym['synonyms'][:10]}")
        else:
            print("Sorry, no synonyms found\n")
            self.show_defs()

    def show_defs(self):
        if not getattr(self, 'webster_homonyms', None):
            self.webster_homonyms = get_defs(self.spelling)
        if getattr(self, 'webster_homonyms', None):
            for homonym in self.webster_homonyms:
                print(f"<{homonym['word_class']}: {homonym['definition']}>")
        else:
            print(f"Is {self.spelling} a word?")


if __name__ == "__main__":
    print(
        """
         _____ _                                          
        |_   _| |                                         
          | | | |__   ___  ___  __ _ _   _ _ __ _   _ ___ 
          | | | '_ \\ / _ \\/ __|/ _` | | | | '__| | | / __|
          | | | | | |  __/\\__ \\ (_| | |_| | |  | |_| \\__ \\
          \\_/ |_| |_|\\___||___/\\__,_|\\__,_|_|   \\__,_|___/ Rex
        """
            )
    try:
        thesr_word = Word(sys.argv[1])
        thesr_word.show_syns()
    except IndexError:
        thesr_word = Word(get_random_word())
        thesr_word.show_syns()
        print("\nThesaurus Rex Command-Line Usage: thesr.py [word]")