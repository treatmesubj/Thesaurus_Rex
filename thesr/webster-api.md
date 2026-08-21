## definitions
```bash
jq '.[0]' cool-def.json  # homonyms
jq '.[0].fl' cool-def.json  # word class
jq '.[0].shortdef' cool-def.json  # definitions
```

## thesarus
```bash
jq '.[0]' cool-thesr.json  # homonyms
jq '.[0].meta.syns' cool-thesr.json  # synonyms
jq '.[0].fl' cool-thesr.json  # word class
jq '.[0].shortdef' cool-thesr.json  # definitions
```

```bash
jq $(jqshape cool-thesr.json | fzf --print-query --select-1 --preview-window='down:50%' --preview "jq {q} cool-thesr.json") cool-thesr.json
```
