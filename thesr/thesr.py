import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
import random
from spellchecker import SpellChecker
import os
from rich.console import Console
import argparse
import socket
import requests.packages.urllib3.util.connection as urllib3_cn

# from fake_useragent import UserAgent


def _allowed_gai_family():
    # https://github.com/shazow/urllib3/blob/master/urllib3/util/connection.py
    family = socket.AF_INET
    # if urllib3_cn.HAS_IPV6:
    #    family = socket.AF_INET6 # force ipv6 only if it is available
    return family


urllib3_cn.allowed_gai_family = _allowed_gai_family
# headers = {
#    "User-Agent": str(UserAgent().random),
# }


def get_random_word():
    response = requests.get("https://web.archive.org/web/https://www.merriam-webster.com/word-of-the-day/calendar")
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )
    word_elems = soup.select(
        "div.more-words-of-day-container ul.more-wod-items li h2 a"
    )
    words = [word_elem.text for word_elem in word_elems]
    random_word = words[random.randint(0, len(words) - 1)]
    return random_word


def get_defs(word):
    response = requests.get(f"https://web.archive.org/web/https://www.merriam-webster.com/dictionary/{word}")
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )
    dict_entry_elems = soup.select("div[id*='dictionary-entry']")
    word_class_elems = soup.select("div.row.entry-header a.important-blue-link")[
        : len(dict_entry_elems)
    ]
    zipped_elems = zip(dict_entry_elems, word_class_elems)

    homographs = []
    try:
        for dict_entry_elem, word_class_elem in zipped_elems:
            definitions_elems = dict_entry_elem.select("span.dtText")
            word_class = word_class_elem.text
            for definition_elem in definitions_elems:
                definition = definition_elem.text[2:]
                homographs.append({"definition": definition, "word_class": word_class})
        if homographs:
            return homographs
    except Exception:
        return


def get_syns_ants(word):
    response = requests.get(f"https://www.thesaurus.com/browse/{word}")
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )
    definition_blocks = soup.select("#synonyms-antonyms .definition-block")

    homographs = []
    try:
        for defi in definition_blocks:
            synonyms = []
            antonyms = []
            for panel in defi.select(".synonym-antonym-panel"):
                if panel.select_one('.synonym-antonym-panel-label').text == 'Synonyms':
                    synonyms = [s.text.strip() for s in panel.select("a")]
                if panel.select_one('.synonym-antonym-panel-label').text == 'Antonyms':
                    antonyms = [s.text.strip() for s in panel.select("a")]
            homographs.append(
                {
                    "word_class": defi.select_one(".part-of-speech-label").text.strip(),
                    "definition": defi.select_one(".definition").text.strip(),
                    "synonyms": synonyms,
                    "antonyms": antonyms
                }
            )
    except Exception:
        return
    return homographs


def get_etymology(word):
    response = requests.get(f"https://www.etymonline.com/word/{word}")
    soup = BeautifulSoup(response.text, "html.parser")
    class_elems = soup.select(
        "section[class^='prose'] h2"
    )
    etym_elems = soup.select(
        "section[class^='prose'] section"
    )
    zipped_elems = zip(class_elems, etym_elems)
    homographs = []
    for class_elem, etym_elem in zipped_elems:
        homographs.append(
            {"etym_desc": etym_elem.text.rstrip("\n"), "word_class": class_elem.text}
        )
    return homographs


class Word:
    def __init__(self, word, console=None):
        self.spelling = word
        self.thesr_homographs = get_syns_ants(self.spelling)
        self.console = console

    def show_syns(self):
        print(f"[{self.spelling}!]", end="\n\n")
        print(f"---Synonyms{'-'*67}")
        if getattr(self, "thesr_homographs", None):
            for homograph in self.thesr_homographs:
                if self.console:
                    self.console.print(
                        f"[magenta]{{ {homograph['word_class']}: {homograph['definition']} }}[/magenta] [green]==[/green] [green]{homograph['synonyms'][:10]}[/green]"
                    )
                else:
                    print(
                        f"{{ {homograph['word_class']}: {homograph['definition']} }} == {homograph['synonyms'][:10]}"
                    )
        else:
            print("Sorry, no synonyms found")
        print("-" * 80, "\n")

    def show_ants(self):
        print(f"---Antonyms{'-'*67}")
        if getattr(self, "thesr_homographs", None):
            for homograph in self.thesr_homographs:
                if self.console:
                    self.console.print(
                        f"[magenta]{{ {homograph['word_class']}: {homograph['definition']} }}[/magenta] [red]=/=[/red] [red]{homograph['antonyms'][:10]}[/red]"
                    )
                else:
                    print(
                        f"{{ {homograph['word_class']}: {homograph['definition']} }} =/= {homograph['antonyms'][:10]}"
                    )
        else:
            print("Sorry, no antonyms found")
        print("-" * 80, "\n")

    def show_defs(self):
        print(f"---Definitions{'-'*67}")
        if not getattr(self, "webster_homographs", None):
            self.webster_homographs = get_defs(self.spelling)
        if getattr(self, "webster_homographs", None):
            for homograph in self.webster_homographs:
                if self.console:
                    console.print(
                        f"[magenta]{{ {homograph['word_class']}: [/magenta][yellow]{homograph['definition']}[/yellow] [magenta]}}[/magenta]"
                    )
                else:
                    print(f"{{ {homograph['word_class']}: {homograph['definition']} }}")
        else:
            print(f"Sorry, no definitions found for {self.spelling}")
            candidates = SpellChecker().candidates(self.spelling)
            if candidates:
                candidates.discard(self.spelling)
                print(f"Did you mean {candidates}?")
        print("-" * 80, "\n")

    def show_etymology(self):
        print(f"---Etymology{'-'*67}")
        if not getattr(self, "etymology", None):
            self.etymology = get_etymology(self.spelling)
        if getattr(self, "etymology", None):
            for homograph in self.etymology:
                if self.console:
                    console.print(
                        f"[magenta]{homograph['word_class']}[/magenta]:\n    [white]{homograph['etym_desc']}[/white]\n{'-'*20}"
                    )
                else:
                    print(
                        f"{homograph['word_class']}:\n    {homograph['etym_desc']}\n{'-'*20}"
                    )
        else:
            print("Sorry, no etymology found")
        print("-" * 80, "\n")


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

    parser = argparse.ArgumentParser()
    parser.add_argument("--word", "-w", action="store")
    parser.add_argument("--define", "-d", action="store_true")
    parser.add_argument("--etymology", "-e", action="store_true")
    parser.add_argument("--antonyms", "-a", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.word:
        thesr_word = Word(args.word, console)
    else:
        thesr_word = Word(get_random_word(), console)

    thesr_word.show_syns()

    if args.define or args.verbose:
        thesr_word.show_defs()
    if args.etymology or args.verbose:
        thesr_word.show_etymology()
    if args.antonyms or args.verbose:
        thesr_word.show_ants()
