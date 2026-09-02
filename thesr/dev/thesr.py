#!/usr/bin/env python
import os
import json
from jq import jq
import requests
import argparse
from rich.console import Console


if __name__ == "__main__":
    console = Console()

    parser = argparse.ArgumentParser()
    parser.add_argument("--word", "-w", action="store", required=True)
    parser.add_argument("--antonyms", "-a", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    websterthesrapikey = os.getenv("websterthesrapikey")

    response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{args.word}?key={websterthesrapikey}")

    if response.text.count('{') == 0:
        print(response.text)
        exit(1)

    sanjay = json.loads(response.text)
    sanjay = jq("""
        [
        .[] | .["def"].[0].["sseq"].[].[0].[1].fl = .fl | .["def"].[0].["sseq"].[].[0].[1] |
            {
                fl: .fl,
                def: (.dt.[0].[-1] | rtrim),
                syns: ([.syn_list.[]?.[].wd] | .[:10]),
                ants: ([.ant_list.[]?.[].wd] | .[:10])
            }
        ]
    """).transform(sanjay)

    console.print(f"\n[bright_yellow]\[{args.word}!][/bright_yellow]", end="\n\n")

    for homograph in sanjay:
        console.print(f"[bright_magenta]({homograph['fl']})[/bright_magenta] [bright_cyan]{homograph['def']}[/bright_cyan]")
        if not args.antonyms:
            console.print(f"\t[bright_green]synonyms: {homograph['syns']}[/bright_green]")
        if args.antonyms or args.verbose:
            console.print(f"\t[bright_red]antonyms: {homograph['ants']}[/bright_red]")
        print('\n')
