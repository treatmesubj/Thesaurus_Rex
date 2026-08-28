## definitions
```bash
jq '.[0]' cool-def.json  # homographs
jq '.[0].fl' cool-def.json  # word class
jq '.[0].shortdef' cool-def.json  # definitions
```

## thesarus
```bash
jq '[.[] | {fl, shortdef, syns: .meta.syns}]' cool-thesr.json
jq '[
    .[] | .["def"].[0].["sseq"].[].[0].[1].fl = .fl | .["def"].[0].["sseq"].[].[0].[1] |
        {
            fl: .fl,
            def: (.dt.[0].[-1] | rtrim),
            syns: ([.syn_list.[]?.[].wd] | .[:10]),
            ants: ([.ant_list.[]?.[].wd] | .[:10])
        }
]' cool-thesr.json > tmp.json
jq -r '.[] | "(" + .fl + ") " + .def +
    "\n\tsynonyms: " + (.syns | join(", ")) +
    "\n\tantonyms: " + (.ants | join(", ")) +
    "\n"' < tmp.json

jq '.[0]' cool-thesr.json  # homographs
jq '.[0].shortdef' cool-thesr.json  # definitions
jq '.[0].meta.syns' cool-thesr.json  # synonyms
jq '.[0].fl' cool-thesr.json  # word class
```

```python
#!/usr/bin/env python3
import json
from rich.console import Console


console = Console()
with open('./tmp.json', 'r') as f:
   data = f.read()

sanjay = json.loads(data)
for homograph in sanjay:
    console.print(f"[bright_magenta]({homograph['fl']})[/bright_magenta] [bright_cyan]{homograph['def']}[/bright_cyan]")
    console.print(f"\t[bright_green]synonyms: {homograph['syns']}[/bright_green]")
    console.print(f"\t[bright_red]antonyms: {homograph['ants']}[/bright_red]\n")
```
