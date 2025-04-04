import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
import random
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
    response = requests.get("https://www.merriam-webster.com/word-of-the-day/calendar")
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
    response = requests.get(f"https://www.merriam-webster.com/dictionary/{word}")
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )
    dict_entry_elems = soup.select("div[id*='dictionary-entry']")
    word_class_elems = soup.select("div.row.entry-header a.important-blue-link")[
        : len(dict_entry_elems)
    ]
    zipped_elems = zip(dict_entry_elems, word_class_elems)

    homonyms = []
    try:
        for dict_entry_elem, word_class_elem in zipped_elems:
            definitions_elems = dict_entry_elem.select("span.dtText")
            word_class = word_class_elem.text
            for definition_elem in definitions_elems:
                definition = definition_elem.text[2:]
                homonyms.append({"definition": definition, "word_class": word_class})
        if homonyms:
            return homonyms
    except Exception:
        return


def get_syns_ants(word):
    response = requests.get(f"http://www.thesaurus.com/browse/{word}")
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )
    script_elem = soup.select_one("script#preloaded-state")
    script = re.search(r"window.__PRELOADED_STATE__ = ({.*})", script_elem.text).group(
        1
    )
    # clean JSON
    script = script.replace(":undefined", ':"undefined"')
    script = script.replace(":null", ':"null"')

    sanjay = json.loads(script)

    homonyms = []
    try:
        posTabs = sanjay["lexigraph"]["thesaurusData"]["data"]["slugs"][0]["entries"][
            -1
        ]["partOfSpeechGroups"]
        for pos in posTabs:
            for defi in pos["shortDefinitions"]:
                homonyms.append(
                    {
                        "word_class": pos["partOfSpeech"],
                        "definition": defi["shortDef"],
                        "synonyms": [s["targetWord"] for s in defi["synonyms"]],
                        "antonyms": [s["targetWord"] for s in defi["antonyms"]],
                    }
                )
        # .lexigraph.thesaurusData.data.slugs[0].entries[-1].partOfSpeechGroups[0].shortDefinitions[0].synonyms[1].targetSlug
    except Exception:
        return
    return homonyms


def get_etymology(word):
    response = requests.get(f"https://www.etymonline.com/word/{word}")
    soup = BeautifulSoup(response.text, "html.parser")
    class_elems = soup.select(
        "section[class^='prose'] [id^='#etymonline']"
    )
    etym_elems = soup.select(
        "section[class^='prose'] section"
    )
    zipped_elems = zip(class_elems, etym_elems)
    homonyms = []
    for class_elem, etym_elem in zipped_elems:
        homonyms.append(
            {"etym_desc": etym_elem.text.rstrip("\n"), "word_class": class_elem.text}
        )
    return homonyms


def get_spell_check_candidates(word):
    response = requests.get(f"https://www.merriam-webster.com/dictionary/{word}")
    soup = BeautifulSoup(response.text, "html.parser")
    candidate_elems = soup.select("p.spelling-suggestions")
    candidates = [c.text for c in candidate_elems]
    return candidates


class Word:
    def __init__(self, word, console=None):
        self.spelling = word
        self.thesr_homonyms = get_syns_ants(self.spelling)
        self.console = console

    def show_syns(self):
        print(f"[{self.spelling}!]", end="\n\n")
        print(f"---Synonyms{'-'*67}")
        if getattr(self, "thesr_homonyms", None):
            for homonym in self.thesr_homonyms:
                if self.console:
                    self.console.print(
                        f"[magenta]{{ {homonym['word_class']}: {homonym['definition']} }}[/magenta] [green]==[/green] [green]{homonym['synonyms'][:10]}[/green]"
                    )
                else:
                    print(
                        f"{{ {homonym['word_class']}: {homonym['definition']} }} == {homonym['synonyms'][:10]}"
                    )
        else:
            print("Sorry, no synonyms found")
        print("-" * 80, "\n")

    def show_ants(self):
        print(f"---Antonyms{'-'*67}")
        if getattr(self, "thesr_homonyms", None):
            for homonym in self.thesr_homonyms:
                if self.console:
                    self.console.print(
                        f"[magenta]{{ {homonym['word_class']}: {homonym['definition']} }}[/magenta] [red]=/=[/red] [red]{homonym['antonyms'][:10]}[/red]"
                    )
                else:
                    print(
                        f"{{ {homonym['word_class']}: {homonym['definition']} }} =/= {homonym['antonyms'][:10]}"
                    )
        else:
            print("Sorry, no antonyms found")
        print("-" * 80, "\n")

    def show_defs(self):
        print(f"---Definitions{'-'*67}")
        if not getattr(self, "webster_homonyms", None):
            self.webster_homonyms = get_defs(self.spelling)
        if getattr(self, "webster_homonyms", None):
            for homonym in self.webster_homonyms:
                if self.console:
                    console.print(
                        f"[magenta]{{ {homonym['word_class']}: [/magenta][yellow]{homonym['definition']}[/yellow] [magenta]}}[/magenta]"
                    )
                else:
                    print(f"{{ {homonym['word_class']}: {homonym['definition']} }}")
        else:
            print("Sorry, no definitions found")
            candidates = get_spell_check_candidates(self.spelling)
            print(f"Did you mean {candidates}?")
        print("-" * 80, "\n")

    def show_etymology(self):
        print(f"---Etymology{'-'*67}")
        if not getattr(self, "etymology", None):
            self.etymology = get_etymology(self.spelling)
        if getattr(self, "etymology", None):
            for homonym in self.etymology:
                if self.console:
                    console.print(
                        f"[magenta]{homonym['word_class']}[/magenta]:\n    [white]{homonym['etym_desc']}[/white]\n{'-'*20}"
                    )
                else:
                    print(
                        f"{homonym['word_class']}:\n    {homonym['etym_desc']}\n{'-'*20}"
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
