## definitions
```bash
jq '.[0]' cool-def.json  # homonyms
jq '.[0].fl' cool-def.json  # word class
jq '.[0].shortdef' cool-def.json  # definitions
```

## thesarus
```bash
jq '[.[] | {fl, shortdef, syns: .meta.syns}]' cool-thesr.json
jq '.[].["def"].[0].["sseq"].[].[0].[1] | {def: (.dt.[0].[-1] | rtrim), syns: ([.syn_list.[]?.[].wd] | .[:10])}' cool-thesr.json

jq '.[0]' cool-thesr.json  # homonyms
jq '.[0].shortdef' cool-thesr.json  # definitions
jq '.[0].meta.syns' cool-thesr.json  # synonyms
jq '.[0].fl' cool-thesr.json  # word class
```
