# Scrabble

This contains code to create a record of hooks and alphagrams out of a word list. It then allows that record to be saved as a database and used as quizzes. These programs began as a way to teach myself python, and was inspired by Zyzzyva, which is now owned by the North American Scrabble(R) Player's Association (NASPA).

## To use the files

* Start with a list of words (spelled in capital letters).
* If the list needs to be updated with additions and/or deletions, use `WordListUpdater.py`
* Run `DictionaryMaker.py` to extract additional information about the word (hooks, the alphagram, number of vowels, etc.) and store in a text file.
* Run `Database0Lexicon.py` to store the information from the text file to a database.
* Run `Database1Users.py` to add a table for different users.
* Run `Database2Lister.py` to create word lists to aid in studying.
    - There are also tools to search the word lists in `Database2Lister.py`
* Make your own version of `Database_WordLister.py` (Using an underscore for `Database_WordLister_<yourname>.py) to generate your favorite word lists for studying.
* Run `Database3Quizzer.py` to quiz yourself on hooks and anagrams!
    - These quizzes will show the words with probabilities such that questions you get wrong or have not yet seen appear less often.
