# Thesaurus Rex
It's a command-line thesaurus tool that uses thesaurus.com's HTML to define a word's homonyms and present their synonyms via HTTP requests, CSS selector, regular expression, and JSON. (It's also a dictionary that uses merriam-webster.com)

### Setup
cd/ into dir of the script or just put it on your system's PATH so you can use it from anywhere

### Usage

`thesr.py [word] [-d | -define]`

If `thesr.py [word]` is too tedious, you can call thesr.exe to call thesr.py for you: `thesr [word]`

If you call `thesr` without a word argument, it'll use a random word from Webster's recent words of the day

If no synonyms for the word can be found, it'll return Webster's definitions

![alt text](https://github.com/treatmesubj/Thesaurus_Rex/blob/master/Screenshot%20(24).png)
