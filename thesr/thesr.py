#!/usr/bin/env python
import os
import json
from jq import jq
import requests
import argparse
from rich.console import Console


def thesaurus(word, apikey):
    response = requests.get(
        f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={apikey}"
    )

    if response.text.count("{") == 0:
        return json.loads(f"{{\"error-response\": {response.text}}}")

    sanjay = json.loads(response.text)
    sanjay = jq(
        """
        [
        .[] | .["def"].[0].["sseq"].[].[0].[1].fl = .fl | .["def"].[0].["sseq"].[].[0].[1] |
            {
                fl: .fl,
                def: (.dt.[0].[-1] | rtrim),
                syns: ([.syn_list.[]?.[].wd] | .[:10]),
                sims: ([.sim_list.[]?.[].wd] | .[:10]),
                ants: ([.ant_list.[]?.[].wd] | .[:10]),
                opps: ([.opp_list.[]?.[].wd] | .[:10])
            }
        ]
    """
    ).transform(sanjay)

    return sanjay


def dictionary(word, apikey):
    response = requests.get(
        f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={apikey}"
    )

    if response.text.count("{") == 0:
        return json.loads(f"{{\"error-response\": {response.text}}}")

    sanjay = json.loads(response.text)
    sanjay = jq(
        """
        [
        map(select(.shortdef | length > 0)).[] |
            {
                "fl": .["fl"],
                "def": .["shortdef"],
                "etymology": .["et"]? // [null] | map(walk(if type == "array" then .[-1] else . end))
            }
        ]
    """
    ).transform(sanjay)

    return sanjay


def rich_console_format(stringy):
    if stringy is None:
        return ""
    return (
        stringy.replace("{it}", "[i]").replace("{/it}", "[/i]")
        .replace("{b}", "[bold]").replace("{/b}", "[/bold]")
    )


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser(
        description="""
stdout:
```

[<word>!]

(<part-of-speech>) <sense-of-word>
    synonyms: []
    antonyms: []

---Dictionary--------------------------------------------------------------------
(<part-of-speech>) <definition>
etymology:
    <etymolgy>
```
        """,
        formatter_class=argparse.RawTextHelpFormatter # Preserves exact formatting
    )
    parser.add_argument("--word", "-w", action="store", required=True)
    parser.add_argument("--antonyms", "-a", action="store_true")
    parser.add_argument("--define", "-d", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    console.print(f"\n[bright_yellow]\[{args.word}!][/bright_yellow]", end="\n\n")

    sanjay = thesaurus(word=args.word, apikey=os.getenv("websterthesrapikey"))

    if 'error-response' in sanjay:
        console.print(sanjay['error-response'])
        sanjay = []

    for homograph in sanjay or []:
        console.print(
            f"[bright_magenta]({homograph['fl']})[/bright_magenta] [bright_cyan]{rich_console_format(homograph['def'])}[/bright_cyan]"
        )
        if not args.antonyms:
            if len(homograph["syns"]) >= len(homograph["sims"]):
                console.print(
                    f"\t[bright_green]synonyms: {homograph['syns']}[/bright_green]"
                )
            else:
                console.print(
                    f"\t[bright_green]near-synonyms: {homograph['sims']}[/bright_green]"
                )
        if args.antonyms or args.verbose:
            if len(homograph["ants"]) >= len(homograph["opps"]):
                console.print(
                    f"\t[bright_red]antonyms: {homograph['ants']}[/bright_red]"
                )
            else:
                console.print(
                    f"\t[bright_red]near-antonyms: {homograph['opps']}[/bright_red]"
                )
        print("\n")

    if args.define or args.verbose:
        print(f"---Dictionary{'-'*68}")
        sanjay = dictionary(word=args.word, apikey=os.getenv("websterdictapikey"))

        if 'error-response' in sanjay:
            console.print(sanjay['error-response'])
            sanjay = []

        for homograph in sanjay or []:
            console.print(
                f"[bright_magenta]({homograph['fl']})[/bright_magenta] [bright_cyan]{rich_console_format(homograph['def'][0])}[/bright_cyan]"
            )
            for defi in homograph["def"][1:]:
                console.print(
                    f"\t[bright_cyan]{rich_console_format(defi)}[/bright_cyan]"
                )

            if homograph["etymology"][0] is not None:
                console.print(
                    f"[bright_yellow]etymology:\n\t{rich_console_format(homograph['etymology'][0])}[/bright_yellow]"
                )
                for ety in homograph["etymology"][1:]:
                    console.print(
                        f"\t[bright_yellow]{rich_console_format(ety)}[/bright_yellow]"
                    )
            print("\n")
