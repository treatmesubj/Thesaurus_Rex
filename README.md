# Thesaurus Rex
Thesaurus tool that fetches a word's homonyms, synonyms, and antonyms from [Thesaurus.com](https://www.thesaurus.com/). It's also a dictionary tool that fetches definitions from [Webster](https://www.merriam-webster.com/)

### Installation
- from [PyPI](https://pypi.org/project/thesr): `pip install thesr`
- from [GitHub](https://github.com/treatmesubj/Thesaurus_Rex): `pip install "git+https://github.com/treatmesubj/Thesaurus_Rex"`

### Usage

```
python -m thesr.thesr [-h] [--word WORD] [--define | --antonyms | --verbose]
```
Common English phrases such as `toungue-and-cheek` or `dime-a-dozen` can be defined and return synonyms as well if Webster and Thesaurus.com have entries for them. 

```
john@spectre:~
$ python -m thesr.thesr --word purport --verbose

         _____ _
        |_   _| |
          | | | |__   ___  ___  __ _ _   _ _ __ _   _ ___
          | | | '_ \ / _ \/ __|/ _` | | | | '__| | | / __|
          | | | | | |  __/\__ \ (_| | |_| | |  | |_| \__ \
          |_| |_| |_|\___||___/\__,_|\__,_|_|   \__,_|___/ Rex

[purport!]

---Synonyms-------------------------------------------------------------------
{ noun: meaning, implication } ==> ['acceptation', 'aim', 'bearing', 'burden', 'connotation', 'core', 'design', 'drift', 'gist', 'heart']
{ verb: assert, mean } ==> ['imply', 'pose as', 'pretend', 'profess', 'allege', 'betoken', 'claim', 'convey', 'declare', 'denote']
--------------------------------------------------------------------------------

---Definitions-------------------------------------------------------------------
{ verb: to have the often specious appearance of being, intending, or claiming (something implied or inferred) }
{ verb: claim  }
{ verb: intend, purpose }
{ noun: meaning conveyed, professed, or implied : import }
{ noun: substance, gist }
--------------------------------------------------------------------------------

---Antonyms-------------------------------------------------------------------
{ noun: meaning, implication } =/=> ['exterior', 'exteriority', 'insignificance', 'meaninglessness', 'outside', 'surface']
{ verb: assert, mean } =/=> ['conceal', 'deny', 'disclaim', 'hide']
--------------------------------------------------------------------------------
```
