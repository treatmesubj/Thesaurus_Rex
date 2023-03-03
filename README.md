# Thesaurus Rex
It's a command-line thesaurus tool that fetches a word's homonyms, synonyms, and antonyms from [Thesaurus.com](https://www.thesaurus.com/) via HTTP requests, CSS selectors, regular expressions, and JSON. It's also a dictionary tool that fetches definitions from [Webster](https://www.merriam-webster.com/)

### Installation
- from [PyPI](https://pypi.org/project/thesr): `pip install thesr`
- from [GitHub](https://github.com/treatmesubj/Thesaurus_Rex): `pip install "git+https://github.com/treatmesubj/Thesaurus_Rex`

### Usage

```
python -m thesr.thesr [-h] [--word WORD] [--define | --antonyms | --verbose]
```

If you call `thesr` without a word argument, it'll fetch a random word from Webster's recent words of the day and fetch its synonyms & antonyms

Common English phrases can be defined and return synonyms as well. Pass the hyphenated phrase as an argument to thesr like so: `thesr tongue-and-cheek -d` or `thesr dime-a-dozen`. Webster seems to have sufficient documentation for common idioms and phrases while Thesaurus.com does too, but to a lesser extent. 

An argument that yields neither synonyms nor a definition is likely misspelled and will return a list of potentially intended words.

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
