# This is a file that will take my current lexicon, and convert it to a table in my database.

import sqlite3

def db_connector(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return(conn)
    except sqlite3.Error as e:
        print(e)
    
    return(None)

def create_table(conn, create_table_sql):
    """ creates a table from the 'create_table_sql' statement
    :param conn: a connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


# I will not worry about Collins, for now.
def create_entry(conn, entryrow, lexicon = 'twl'):
    #Creating a new gram
    sql = 'INSERT INTO lexicon_' + lexicon +\
          '''(gram, word, length, score, vowels, threeplus, jqxz, remfirst, remlast,\
              fhook, bhook, nrack, nrack_adj)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entryrow)
    return(cur.lastrowid)


def alphasort(string):
    list = []
    for ltr in string:
        list.append(ltr)
    list.sort()
    output = ''
    for ltr in list:
        output = output + ltr
    return(output)

# Opening the database
database = "Scrabble_Database.db"
conn = db_connector(database)

# First step: creating the table

def lex_table(lexicon):
    lexicon_table = 'CREATE TABLE IF NOT EXISTS lexicon_' + lexicon +\
                    	'''(gram text NOT NULL,
                            word text PRIMARY KEY,
                            length integer,
                            score integer,
                            vowels integer,
                            threeplus integer,
                            jqxz integer,
                            remfirst integer,
                            remlast integer,
                            fhook text,
                            bhook text,
                            nrack integer,
                            nrack_adj integer
                            );'''
    
    if conn is not None:
        create_table(conn, lexicon_table)
        conn.commit()

def lex_table_delete(lexicon):
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS lexicon_'+lexicon)
    conn.commit()




# Second Step: adding the words

def multicount(string, ltrs):
    output = 0
    for ltr in ltrs:
        output += string.count(ltr)
    return (output)

# Adding functions, because I would like probability to be included
def factorial(n):
    ans = 1
    for k in range(n):
        ans = ans*(k+1)
    return ans

def choose(a,b):
    num = 1
    denom = 1
    stoopidity = False
    if ((a < b) or (b < 0)):
        stoopidity = True
        ans = 0
    elif b <= a//2:
        for i in range((a-b),a):
            num = num * (i+1)
        denom = factorial(b)
    else:
        for i in range(b,a):
            num = num * (i+1)
        denom = factorial(a-b)
    if not stoopidity:
        ans = num//denom
    return ans

# Maybe I should allow this to be specified as well
# ... something to edit later.
TileBag = {'E':12, 'A':9, 'I':9, 'O':8, 'U':4, 'S':4,\
           'R':6, 'T':6, 'N':6, 'L':4, 'D':4, 'G':3,\
           'P':2, 'M':2, 'B':2, 'H':2, 'F':2, 'W':2,\
           'Y':2, 'K':1, 'C':2, 'V':2, 'X':1, 'J':1,\
           'Z':1, 'Q':1, '?':2}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def numracks(rack):
    Rack = rack.upper()
    rackList = []
    for char in Rack:
        rackList.append(char)
    rackList.sort()
    num = choose(TileBag[rackList[0]],rackList.count(rackList[0]))
    for ctr in range(1,len(rackList)):
        if rackList[ctr] != rackList[ctr-1]:
            x = choose(TileBag[rackList[ctr]],rackList.count(rackList[ctr]))
            num *= x
    return num

def numracksadj(rack):
    Rack = rack.upper()
    nr = numracks(Rack)
    esses = Rack.count('S')
    if esses == 1:
        nr = nr*1.5
    elif esses > 1:
        nr = nr * 2
    return nr

# This is a function that could be useful
# I stole this from StemStringer.py
def substrings(tiles, num):
    # Checking input and sorting letters in order
    accept, output = True, []
    tiles = tiles.upper()
    for x in tiles:
        if alphabet.count(x) == 0:
            accept = False
            break
    if accept:
        tiles = alphasort(tiles)
        matrix = []
        k,l,r = 0,0,1
        list = [0]
        tileset = []
        while k < len(tiles):
            tileset.append(tiles[k])
            k += tiles.count(tiles[k])
            while r < k:
                list.append(l)
                r += 1
            l += 1
        minlist = list[:num]
        maxlist = list[-num:]
        # starting to loop through the list
        go = True
        ctr = 0
        curlist = []
        for x in minlist:
            curlist.append(x)
        while go:
            output.append('')
            for x in curlist:
                output[ctr] += tileset[x]
            # Checking to see if we have reached the highest value
            if curlist[0] == maxlist[0]:
                i = curlist[0] + 1
                try:
                    if curlist.index(i) == maxlist.index(i):
                        go = False
                        break
                except ValueError:
                    go = False
                    break
            # Going to the next value if possible
            # There are necessary hacks in this code
            # I first tried to change the individual indices of curlist
            # But that just changed the value of q
            if curlist[-1] == maxlist[-1]:
                j = num - 2
                while curlist[j] == maxlist[j]:
                     j -= 1
                curlist[j] += 1
                curlist = curlist[:j+1]
                while j < num-1:
                    j += 1
                    q = curlist[-1]
                    if j-curlist.index(q) < list.count(q):
                        curlist.append(q)
                    else:
                        curlist.append(q+1)
            else:
                curlist[-1] += 1
            ctr += 1
            
    return output

def numracksblank(rack, blanks = 2):
    bkmax = min(blanks, len(rack))
    num = numracks(rack)
    for bk in range(1,bkmax+1):
        if bk < len(rack):
            subracks = substrings(rack, len(rack)-bk)
            for sbrk in subracks:
                num += choose(blanks, bk)*numracks(sbrk)
        else:
            num += choose(blanks, bk)
    return(num)

def numracksblankadj(rack, blanks = 2):
    bkmax = min(blanks, len(rack))
    num = numracksadj(rack)
    for bk in range(1,bkmax+1):
        if bk < len(rack):
            subracks = substrings(rack, len(rack)-bk)
            for sbrk in subracks:
                num += choose(blanks, bk)*numracks(sbrk)
        else:
            num += choose(blanks, bk)
    return(num)



def lex_db(lexicon):
    file = open('Words/UpdatedDic_' + lexicon + '.txt', 'r')
    x = 1
    for line in file:
        line = line.rstrip('\n')
        if line.strip(' ') == '':
            continue
        line = line.split(',')
        length = len(line[0])
        nv = line[0].count('A') + line[0].count('E') + line[0].count('I') + \
            line[0].count('O') + line[0].count('U')
        njqxz = line[0].count('J') + line[0].count('Q') + line[0].count('X') + line[0].count('Z')
        ntp = multicount(line[0], 'BCFHKMPVWY') + njqxz
        pts = nv + multicount(line[0], 'LNRST') + 2*multicount(line[0], 'DG') +\
              3*multicount(line[0], 'BCMP') + 4*multicount(line[0], 'FHVWY') + 5*line[0].count('K') +\
              8*multicount(line[0], 'JX') + 10*multicount(line[0],'QZ')
        gram = alphasort(line[0])
        nrack = numracksblank(line[0])
        nrack_adj = numracksblankadj(line[0])
        with conn:
            entry = (gram, line[1], length, pts, nv, ntp, njqxz, int(line[4]=='y'), int(line[5]=='y'),\
                     line[2], line[3], nrack, nrack_adj)
            create_entry(conn, entry, lexicon = lexicon)
        if x%10000 == 0:
            print(x)
        x += 1
    print(x)
    file.close()
    conn.commit()

# This seems to have worked!

