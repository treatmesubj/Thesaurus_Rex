# Thesaurus-Rex
Thesaurus tool that fetches a word's homonyms, synonyms, and antonyms from [Thesaurus.com](https://www.thesaurus.com/). It's also a dictionary tool that fetches definitions from [Webster](https://www.merriam-webster.com/). It fetches etymology information from [etymonline](https://www.etymonline.com/).

### Installation
- from [PyPI](https://pypi.org/project/thesr): `pip install thesr`
- from [GitHub](https://github.com/treatmesubj/Thesaurus_Rex): `pip install "git+https://github.com/treatmesubj/Thesaurus_Rex"`

### Usage

```
python -m thesr.thesr [-h] [--word WORD] [--define] [--etymology] [--antonyms] [--verbose]
```
Common English phrases & idioms such as `toungue-and-cheek` or `dime-a-dozen` sometimes work as well

```
john@spectre:~
$ python -m thesr.thesr -w purport -v

         _____ _
        |_   _| |
          | | | |__   ___  ___  __ _ _   _ _ __ _   _ ___
          | | | '_ \ / _ \/ __|/ _` | | | | '__| | | / __|
          | | | | | |  __/\__ \ (_| | |_| | |  | |_| \__ \
          |_| |_| |_|\___||___/\__,_|\__,_|_|   \__,_|___/ Rex

[purport!]

---Synonyms-------------------------------------------------------------------
{ noun: meaning, implication } == ['acceptation', 'aim', 'bearing', 'burden', 'connotation', 'core', 'design',
'drift', 'gist', 'heart']
{ verb: assert, mean } == ['imply', 'pose as', 'pretend', 'profess', 'allege', 'betoken', 'claim', 'convey',
'declare', 'denote']
--------------------------------------------------------------------------------

---Definitions-------------------------------------------------------------------
{ verb: to have the often specious appearance of being, intending, or claiming (something implied or inferred) }
{ verb: claim  }
{ verb: intend, purpose }
{ noun: meaning conveyed, professed, or implied : import }
{ noun: substance, gist }
--------------------------------------------------------------------------------

---Etymology-------------------------------------------------------------------
purport (n.)
    early 15c., "meaning, tenor, the surface or expressed meaning of a document, etc.; that which is conveyed or
expressed," from Anglo-French purport (late 13c.), Old French porport "contents, tenor," back-formation from
purporter "to contain, convey, carry; intend," from pur- (from Latin pro- "forth;" see pur-) + Old French porter "tocarry," from Latin portare "to carry" (from PIE root *per- (2)  "to lead, pass over"). Meaning "that which is to be done or effected" is from 1650s.
--------------------
purport (v.)
    1520s, "indicate, express, set forth, convey to the mind as the meaning or thing intended," from the noun in Englishand from Anglo-French purporter (c. 1300), from Old French purporter "to contain, convey, carry; intend," from pur- (from Latin pro- "forth;" see pur-) + Old French porter "to carry," from Latin portare "to carry" (from PIE root
*per- (2)  "to lead, pass over"). Related: Purported; purporting.
--------------------------------------------------------------------------------

---Antonyms-------------------------------------------------------------------
{ noun: meaning, implication } =/= ['exterior', 'exteriority', 'insignificance', 'meaninglessness', 'outside',
'surface']
{ verb: assert, mean } =/= ['conceal', 'deny', 'disclaim', 'hide']
--------------------------------------------------------------------------------
```
