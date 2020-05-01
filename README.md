# Thesaurus Rex
It's a command-line thesaurus tool that uses thesaurus.com's HTML to determine a word's homonyms and present their synonyms via HTTP requests, CSS selectors, regular expressions, and JSON. (It's also a dictionary that uses merriam-webster.com)

### Setup
cd/ into dir of the script or just put it on your system's PATH so you can use it from anywhere

### Usage

`thesr.py [word | hyphenated-phrase] [-d | --define]`

If `thesr.py [word]` is too tedious, you can call thesr.exe to call thesr.py for you: `thesr [word]`

If you call `thesr` without a word argument, it'll use a random word from Webster's recent words of the day

Common English phrases can be defined and return synonyms as well. Pass the hyphenated phrase as an argument to thesr like so: `thesr tongue-and-cheek -d` or `thesr dime-a-dozen`. Webster seems to have sufficient documentation for common idioms and phrases while thesaurus.com does too, but to a lesser extent. 

![alt text](https://github.com/treatmesubj/Thesaurus_Rex/blob/master/Screenshot%20(24).png)
