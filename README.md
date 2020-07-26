# Scrabble

This contains code to create a record of hooks and alphagrams out of a word list. It then allows that record to be saved as a database and used as quizzes. These programs began as a way to teach myself python, and was inspired by Zyzzyva, which is now owned by the North American Scrabble(R) Player's Association (NASPA).

## To use the files

* Start with a list of words (spelled in capital letters).
* If the list needs to be updated with additions and/or deletions, use `WordListUpdater.py`
* Run `DictionaryMaker.py` to extract additional information about hooks and anagrams
* Run `Database0Lexicon.py` to create a database to store the words.
* Run `Database1Users.py` to add a table for different users.
* Run `Database2Lister.py` to create word lists to aid in studying.
    - There are also tools to search the word lists in `Database2Lister.py`
* Run `Database3Quizzer.py` to quiz yourself on hooks and anagrams!
