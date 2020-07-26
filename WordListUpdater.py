# A file to update a word list with additions and deletions

# Importing the original word List
words_orig = file.open('Words/words_orig', 'r')
list_orig = []
for line in words_orig:
  word = line.strip('\r')
  word = word.strip('\n')
  word = word.upper()
  list_orig.append(word)
words_orig.close()

# Additions
words_add = file.open('Words/words_add', 'r')
list_add = []
for line in words_add:
  word = line.strip('\r')
  word = word.strip('\n')
  word = word.upper()
  list_add.append(word)
words_add.close()

# Deletions
words_del = file.open('Words/words_del', 'r')
list_del = []
for line in words_del:
  word = line.strip('\r')
  word = word.strip('\n')
  word = word.upper()
  list_del.append(word)
words_del.close()

# Creating place for new list
list_new = []
list_new.extend(list_orig)

# Deleting deletions
for word in list_del:
  while list_new.count(word) > 0:
    list_new = list_new.remove(word)

# Adding additions
list_new.extend(list_add)

# Sorting the list
list_new.sort()

# Writing to a file
words_new = file.open('Words/UpdatedWordList', 'w')
for word in list_new:
  words_new.write(word + '\n\r')

# I think this is it.





