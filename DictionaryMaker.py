# This is a file that will build the dictionary
# ... with the information I want from a wordlist
# ... chosen by the user.

# Other than this comment, this is exactly the
# ... version on github.

# Importing the os module
import os


# These converters will be changed when I figure out
# a good way to have a user specified ordering of the tiles.

# I have currently decided to save everything as alphabetical
# and allow for different ordering when these are saved to databases.

tilecount = {'A':9,'B':2,'C':2,'D':4,'E':12,'F':2,'G':3,\
             'H':2,'I':9,'J':1,'K':1,'L':4,'M':2,'N':6,\
             'O':8,'P':2,'Q':1,'R':6,'S':4,'T':6,'U':4,\
             'V':2,'W':2,'X':1,'Y':2,'Z':1,'?':2}


# Writing functions
# Sorting letters in alphabetical order
def alphasort(word):
    listword = []
    for letr in word:
        listword.append(letr)
    listword.sort()
    output = ''
    for letr in listword:
        output = output + letr
    return(output)



def text_data_add(filename):
    # Opening a file that lists all words in a text document
    allwords = []
    wordsfile = open('Words/' + filename)
    for line in wordsfile:
        line = line.rstrip(' \r\n')
        line = line.upper()
        if len(line) > 1:
            allwords.append(line)
    wordsfile.close()
    
    # Adding data to the words
    masterlist = []
    Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for word in allwords:
        letters = []
        wordData = [len(word)]
        # Putting a letter in alphabetical order
        alphagram = alphasort(word)
        wordData.append(alphagram)
        wordData.append(word)
        wordData.extend(['','',False,False])
        masterlist.append(wordData)
    
    print('Words Added!')
    print(len(masterlist))
    
    # Adding front and back hook data
    for x in range(len(masterlist)):
        word = masterlist[x][2]
        if len(word) > 2:
            first = word[0]
            firstgone = word[1:]
            last = word[-1]
            lastgone = word[:-1]
            try:
                q = allwords.index(firstgone)
                masterlist[q][3] += first
                masterlist[x][5] = True
            except ValueError:
                pass
            try:
                q = allwords.index(lastgone)
                masterlist[q][4] += last
                masterlist[x][6] = True
            except ValueError:
                pass
        if x%10000 == 0:
            print(x)
    print(x)
    
    masterlist.sort()
    
    print('Word data added!')
    
    # Sorting the hooks.
    x = 0
    for data in masterlist:
        masterlist[x][3] = alphasort(masterlist[x][3])
        masterlist[x][4] = alphasort(masterlist[x][4])
        x += 1
    
    print(len(masterlist))
    
    # Adding words to the dicanary
    dicanary = open('Words/UpdatedDic', 'w')
    
    for data in masterlist:
        for k in range(1,5):
            script = data[k]
            dicanary.write(script)
            dicanary.write(',')
        if data[5]:
            dicanary.write('y,')
        else:
            dicanary.write('n,')
        if data[6]:
            dicanary.write('y')
        else:
            dicanary.write('n')
        dicanary.write('\r\n')
    dicanary.close()
    
    print('Process Complete!')


