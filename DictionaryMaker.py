# This is a file that will build the dictionary
# ... with the information I want from a wordlist
# ... chosen by the user.

# Right now, this is a bit of a dump, but I hope to make it more organized

import os

# Opening a file that lists all words in a text document
allwords = []
wordsfile = open('Words/twl2018-dos.txt')
for line in wordsfile:
    line = line.rstrip('\r\n')
    line = line.upper()
    allwords.append(line)
wordsfile.close()


# These converters will be changed when I figure out
# a good way to have a user specified ordering of the tiles.

# I have currently decided to save everything as alphabetical
# and allow for different ordering when these are saved to databases.
userlton = {'E':1,'A':2,'I':3,'O':4,'U':5,'S':6,\
              'R':7,'T':8,'N':9,'L':10,'D':11,'G':12,\
              'P':13,'M':14,'B':15,'H':16,'F':17,'W':18,\
              'Y':19,'K':20,'C':21,'V':22,'X':23,'J':24,\
              'Z':25,'Q':26}
userntol = {1:'E',2:'A',3:'I',4:'O',5:'U',6:'S',\
              7:'R',8:'T',9:'N',10:'L',11:'D',12:'G',\
              13:'P',14:'M',15:'B',16:'H',17:'F',18:'W',\
              19:'Y',20:'K',21:'C',22:'V',23:'X',24:'J',\
              25:'Z',26:'Q'}
tilecount = {'A':9,'B':2,'C':2,'D':4,'E':12,'F':2,'G':3,\
             'H':2,'I':9,'J':1,'K':1,'L':4,'M':2,'N':6,\
             'O':8,'P':2,'Q':1,'R':6,'S':4,'T':6,'U':4,\
             'V':2,'W':2,'X':1,'Y':2,'Z':1,'?':2}

''' 
def convertlton(list):
    output = []
    for x in range(4):
        sec = []
        for letr in list[x]:
            sec.append(dscrablton[letr])
        output.append(sec)
    for x in range(4,6):
        output.append(list[x])
    output[0].sort()
    output[2].sort()
    output[3].sort()
    return output

def convertntol(list):
    output = []
    for x in range(4):
        seq = ''
        for num in list[x]:
            seq += dscrabntol[num]
        output.append(seq)
    for x in range(4,6):
        output.append(list[x])
    return output
'''

# Writing functions
# This will stay
def alphasort(word):
    listword = []
    for letr in word:
        listword.append(letr)
    listword.sort()
    output = ''
    for letr in listword:
        output = output + letr
    return(output)

# I do not know if this is useful
def userltonfun(word):
    output = []
    for letr in word:
        output.append(userlton[letr])
    return(output) 

# This will stay
def taxoncode(list):
    output = ''
    for item in list:
        if item < 10:
           output = output + '0' + str(item)
        else:
           output = output + str(item)
    return(output)


# Creating a place to store words in taxa!
taxondic = {}  # This is where the words will be sorted
#wordlist = []  # This is where the words will be kept until I add them to a file
for letrs in range(2,16):
    for blanks in range(0,letrs+1):
        for cons in range(0,letrs+1):
            for hpt in range(0,cons+1):
                for XJZQ in range(0,hpt+1):
                    taxondic[taxoncode([letrs,blanks,cons,hpt,XJZQ])] = []



# Adding and sorting the words to my new list


# import WordJudge


# Adding Data to the words
masterlist = []
Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for word in allwords:
    letters = []
    wordData = [len(word)]
    # Putting a letter in the specified order
    alphagram = alphasort(word)
    wordData.append(alphagram)
    wordData.append(word)
    wordData.extend(['','',False,False])
    masterlist.append(wordData)


# Adding front and back hook data
Lengths = [0]
y = 0
for x in range(len(masterlist)):
    #if x != len(masterlist) - 1:
    #    if masterlist[x][0] != masterlist[x+1][0]:
    #        Lengths.append(x+1)
    #        y += 1
    #else:
    #    Lengths.append(x+1)
    word = masterlist[x][2]
    if len(word) > 2:
        c = 0
        firstgone = ''
        lastgone = ''
        first = ''
        last = ''
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

masterlist.sort()
            

print('Word data added!')

# I'm going to need to edit this to work.
x = 0
for data in masterlist:
    masterlist[x][3] = alphasort(masterlist[x][3])
    masterlist[x][4] = alphasort(masterlist[x][4])
    word = data[2]
    nletr = data[0]
    # There is probably a more elegant way to do this next line.
    nv = word.count('E') + word.count('A') + word.count('I') + word.count('O') + word.count('U')
    nc = nletr - nv
    nhpt = 0
    nXJZQ = 0
    for letr in 'PMBHFWYKCVXJZQ':
        nhpt += word.count(letr)
    for letr in 'XJZQ':
        nXJZQ += word.count(letr)
    nblanks = 0
    for letr in 'EAIOUSRTNLDGPMBHFWYKCVXJZQ':
        if word.count(letr) > tilecount[letr]:
            nblanks += word.count(letr) - tilecount[letr]
    taxondic[taxoncode([nletr,nblanks,nc,nhpt,nXJZQ])].append(data)
    x += 1

print('Taxon dictionary created!')
    

# Putting the words in order, at least by taxon
# Adding a p
tot = 0
taxondicnum = {}
wordlist = []
for letrs in range(2,16):
    for blanks in range(0,letrs+1):
        for cons in range(0,letrs+1):
            for hpt in range(0,cons+1):
                for XJZQ in range(0,hpt+1):
                    if len(taxondic[taxoncode([letrs,blanks,cons,hpt,XJZQ])]) > 0:
                        taxondicnum[taxoncode([letrs,blanks,cons,hpt,XJZQ])] = [tot]
                        tot += len(taxondic[taxoncode([letrs,blanks,cons,hpt,XJZQ])])
                        taxondicnum[taxoncode([letrs,blanks,cons,hpt,XJZQ])].append(tot)
                    temptaxon = []
                    # This is where it is ordered
                    for elt in taxondic[taxoncode([letrs,blanks,cons,hpt,XJZQ])]:
                        elt[0] = userltonfun(elt[1])
                        temptaxon.append(elt)
                    temptaxon.sort()
                    # Now it is being replaced
                    taxondic[taxoncode([letrs,blanks,cons,hpt,XJZQ])] = temptaxon
                    for elt in taxondic[taxoncode([letrs,blanks,cons,hpt,XJZQ])]:
                        wordlist.append(elt)


# Adding words to the dicanary
dicanary = open('Words/UpdatedDic','w')

for data in wordlist:
    for x in range(1,5):
        script = data[x]
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


print(Lengths)



# Adding the taxon dictionary.
file = open('Words/UpdatedTaxa','w')

for entry in taxondicnum:
    file.write(entry + ' ')
    file.write(str(taxondicnum[entry][0]) + ',' + str(taxondicnum[entry][1]) + '\r\n')
file.close()


