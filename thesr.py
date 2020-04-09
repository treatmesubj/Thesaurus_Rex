import requests
import re
import json
import sys


def get_syns(word):

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

    session = requests.session()

    print(f"[{word}!]", end="\n\n")

    url = f"http://www.thesaurus.com/browse/{word}"
    html = session.get(url, headers={"user-agent": "Mozilla/5.0"}).text
    script = re.search(r'<script>window\.INITIAL_STATE = (.+);</script>', html).group(1)

    try:
        j = json.loads(script)
    except json.decoder.JSONDecodeError:
        bitches = [u.start() for u in re.finditer("undefined", script)]
        if len(bitches) > 0:
            script = script.replace('undefined', "\"undefined\"")
        j = json.loads(script)

    posTabs = j['searchData']['tunaApiData']['posTabs']
    for tab in posTabs:
        print(f"<{tab['pos']}: {tab['definition']}> ~~~~~~~~~ {[s['term'] for s in tab['synonyms'][:10]]}")


if __name__ == "__main__":
    get_syns(sys.argv[1])