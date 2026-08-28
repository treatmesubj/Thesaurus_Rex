#!/usr/bin/env bash
usage() {
    echo -e "usage:"
    echo -e "\tthesr [-h] <-w|--word WORD> [-a|--antonyms]"
    exit 1
}

# set variables
set_param_var() {
    if ! [[ (-z "$2" || "$2" =~ ^-.+) ]]; then
        declare -g "$1=$2"
    else
        echo "parameter '$1' provided without a value"
        exit 1
    fi
}

# parse arguments
if [ $# -eq 0 ]; then
    usage
fi

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage ;;
        -w|--word)
            set_param_var "word" "$2" && shift 2; ;;
        -a|--antonyms)
            antonyms=true && shift; ;;
        *)
            echo "invalid parameter: '$1'"
            exit 1
            ;;
    esac
done


response=$(
    curl -s "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/$word?key=$apikey"
)

sanjay=$(jq '[
    .[] | .["def"].[0].["sseq"].[].[0].[1].fl = .fl | .["def"].[0].["sseq"].[].[0].[1] |
        {
            fl: .fl,
            def: (.dt.[0].[-1] | rtrim),
            syns: ([.syn_list.[]?.[].wd] | .[:10]),
            ants: ([.ant_list.[]?.[].wd] | .[:10])
        }
    ]' <<< "$response"
)
data=$(mktemp)
echo "$sanjay" > "$data"

python - << EOF
import json
from rich.console import Console


console = Console()
with open('$data', 'r') as f:
   data = f.read()

sanjay = json.loads(data)
for homograph in sanjay:
    console.print(f"[bright_magenta]({homograph['fl']})[/bright_magenta] [bright_cyan]{homograph['def']}[/bright_cyan]")
    console.print(f"\t[bright_green]synonyms: {homograph['syns']}[/bright_green]")
    console.print(f"\t[bright_red]antonyms: {homograph['ants']}[/bright_red]\n")
EOF
