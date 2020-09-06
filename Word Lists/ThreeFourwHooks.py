import sqlite3
import Database2Lister_lex as d2

def alphasort(str):
    list = []
    for char in str:
        list.append(char)
    list.sort()
    outstr = ''
    for elt in list:
        outstr += elt
    return(outstr)

threefourentries = d2.search_list(['length >= 3', 'length <= 4'],\
                                  lexicon = 'twl')



threefourlist = []
for entry in threefourentries:
    lng = entry[2]
    word = entry[1]
    fh = entry[9]
    bh = entry[10]
    prestr = ' '
    poststr = ' '
    if entry[7] == 1:
        prestr = '-'
    if entry[8] == 1:
        poststr = '-'
    numgram = len(d2.search_anag(word, lexicon = 'twl'))
    threefourlist.append([lng, word, alphasort(fh.lower()),\
                          alphasort(bh.lower()),\
                          prestr, poststr, str(numgram)])
threefourlist.sort()


file = open('Words/HookList34', 'w')
# Determining the length to add spaces
maxf = 0
for x in range(len(threefourlist)):
    maxf = max(len(threefourlist[x][2]), maxf)
print('maxf: ' + str(maxf))
maxb = 0
for x in range(len(threefourlist)):
    maxb = max(len(threefourlist[x][3]), maxb)
print('maxb: ' + str(maxb))


for x in range(len(threefourlist)):
        file.write(' '*(maxf - len(threefourlist[x][2])) + threefourlist[x][2] + ' ' + threefourlist[x][4] +\
                   threefourlist[x][1] + threefourlist[x][5] + threefourlist[x][6] + ' ' +\
                   threefourlist[x][3] + ' '*(maxb-len(threefourlist[x][3])) + '\r')
file.close()
