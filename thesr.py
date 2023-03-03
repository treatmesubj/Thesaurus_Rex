import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
import sys
import random
from spellchecker import SpellChecker
import os
from rich.console import Console


def get_random_word():
    soup = BeautifulSoup(requests.get("https://www.merriam-webster.com/word-of-the-day/calendar").text, 'html.parser')
    word_elems = soup.select("div.more-words-of-day-container ul.more-wod-items li h2 a")
    words = [word_elem.text for word_elem in word_elems]
    random_word = words[random.randint(0, len(words)-1)]
    return random_word


def get_defs(word):
    soup = BeautifulSoup(requests.get(f"https://www.merriam-webster.com/dictionary/{word}").text, 'html.parser')
    dict_entry_elems = soup.select("div[id*='dictionary-entry']")
    word_class_elems = soup.select("div.row.entry-header a.important-blue-link")[:len(dict_entry_elems)]
    zipped_elems = zip(dict_entry_elems, word_class_elems)

    homonyms = []
    try:
        for dict_entry_elem, word_class_elem in zipped_elems:
            definitions_elems = dict_entry_elem.select("span.dtText")
            word_class = word_class_elem.text
            for definition_elem in definitions_elems:
                definition = definition_elem.text[2:]
                homonyms.append({
                    'definition': definition,
                    'word_class': word_class
                    })
        if homonyms:
            return homonyms
    except Exception:
        return


def get_syns_ants(word):
    soup = BeautifulSoup(requests.get(f"http://www.thesaurus.com/browse/{word}", headers={"user-agent": "Mozilla/5.0"}).text, 'html.parser')
    script = re.search(r'<script>[\s\S]*window\.INITIAL_STATE = (.+);[\s\S]*</script>', soup.prettify()).group(1)
    # clean JSON
    script = script.replace(":undefined", ":\"undefined\"")
    script = script.replace(":null", ":\"null\"")

    j = json.loads(script)

    try:
        posTabs = j['searchData']['tunaApiData']['posTabs']
    except TypeError:
        return

    homonyms = []
    for tab in posTabs:
        homonyms.append({
            'word_class': tab['pos'],
            'definition': tab['definition'],
            'synonyms': [s['term'] for s in tab['synonyms']],
            'antonyms': [s['term'] for s in tab['antonyms']]
            })
    return homonyms


class Word:
    def __init__(self, word, console):
        self.spelling = word
        self.thesr_homonyms = get_syns_ants(self.spelling)
        self.console = console

    def show_syns(self):
        print(f"[{self.spelling}!]", end="\n\n")
        print(f"---Synonyms{'-'*67}")
        if getattr(self, "thesr_homonyms", None):
            for homonym in self.thesr_homonyms:
                console.print(f"[magenta]{{ {homonym['word_class']}: {homonym['definition']} }}[/magenta] [green]==>[/green] [green]{homonym['synonyms'][:10]}[/green]")
        else:
            print("Sorry, no synonyms found")
        print('-'*80, '\n')

    def show_ants(self):
        print(f"---Antonyms{'-'*67}")
        if getattr(self, "thesr_homonyms", None):
            for homonym in self.thesr_homonyms:
                console.print(f"[magenta]{{ {homonym['word_class']}: {homonym['definition']} }}[/magenta] [red]=/=>[/red] [red]{homonym['antonyms'][:10]}[/red]")
        else:
            print("Sorry, no antonyms found")
        print('-'*80, '\n')

    def show_defs(self):
        print(f"---Definitions{'-'*67}")
        if not getattr(self, 'webster_homonyms', None):
            self.webster_homonyms = get_defs(self.spelling)
        if getattr(self, 'webster_homonyms', None):
            for homonym in self.webster_homonyms:
                console.print(f"[magenta]{{ {homonym['word_class']}: [/magenta][yellow]{homonym['definition']}[/yellow] [magenta]}}[/magenta]")
        else:
            print(f"Is {self.spelling} a word?")
            candidates = SpellChecker().candidates(self.spelling)
            candidates.discard(self.spelling)
            if candidates:
                print(f"Did you mean {candidates}?")
        print('-'*80, '\n')


if __name__ == "__main__":
    print(
        """
         _____ _                                          
        |_   _| |                                         
          | | | |__   ___  ___  __ _ _   _ _ __ _   _ ___ 
          | | | '_ \\ / _ \\/ __|/ _` | | | | '__| | | / __|
          | | | | | |  __/\\__ \\ (_| | |_| | |  | |_| \\__ \\
          |_| |_| |_|\\___||___/\\__,_|\\__,_|_|   \\__,_|___/ Rex
        """
            )
    console = Console()
    try:
        thesr_word = Word(sys.argv[1], console)
        thesr_word.show_syns()

        if len(sys.argv) > 2:
            if sys.argv[2] in ("-d", "--define"):
                thesr_word.show_defs()
            elif sys.argv[2] in ('-a', '--antonyms'):
                thesr_word.show_ants()
            elif sys.argv[2] in ('-v', '--verbose'):
                thesr_word.show_defs(); thesr_word.show_ants()
            else:
                pass

    except IndexError:
        thesr_word = Word(get_random_word(), console)
        thesr_word.show_syns(); thesr_word.show_defs(); thesr_word.show_ants()
        print("Thesaurus Rex Command-Line Usage: thesr <word|hyphenated-phrase> [-d | --define | -a | --antonyms | -v | --verbose]")

