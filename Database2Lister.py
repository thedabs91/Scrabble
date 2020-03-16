import sqlite3

database = "/home/david/Documents/Common Stuff/PythonPrograms/Scrabble/Users/database.db"
conn = sqlite3.connect(database)

c = conn.cursor()

# I should think about when I would like to recreate the gram_table.
readd = False

if readd:
    c.execute('DROP TABLE IF EXISTS gram_table')

gram_table_sql = '''CREATE TABLE IF NOT EXISTS gram_table(
                        listname text NOT NULL,
                        gram text NOT NULL
                    );'''
c.execute(gram_table_sql)

if readd:
    LPB_sql = 'SELECT * FROM lexicon_twl WHERE length > 6 AND length < 10 AND threeplus = 0'
    LPB_entries = c.execute(LPB_sql)
    LPB_entries = LPB_entries.fetchall()
    prevgram = ''
    for k in range(len(LPB_entries)):
        gram = LPB_entries[k][0]
        add_sql = '''INSERT INTO gram_table(listname, gram)
                     VALUES("LowPtBingo",?)'''
        if gram != prevgram:
            c.execute(add_sql, (LPB_entries[k][0],))
        prevgram = LPB_entries[k][0]
    conn.commit()


# I would also like to think about making the above a function.
# I want to be able to add lists easily.


def strsort(string):
    list = []
    for char in string:
        list.append(char)
    list.sort()
    output = ''
    for elt in list:
        output += elt
    return(output)

def multicount(string, ltrs):
    output = 0
    for ltr in ltrs:
        output += string.count(ltr)
    return (output)

def uniq_let(string):
    string = string.upper()
    output = ''
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if char in string:
            output += char
    return(output)

def let_dic(string):
    string = string.upper()
    str_dic = {}
    for ltr in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        str_dic[ltr] = string.count(ltr)
    return(str_dic)
        

pt_dic = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1,\
          'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,\
          'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,\
          'P': 3, 'Q':10, 'R': 1, 'S': 1, 'T': 1,\
          'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4,\
          'Z':10, '?': 0}

def search_anag(gram):
    gram = gram.upper()
    gram = strsort(gram)
    search_sql = 'SELECT * FROM lexicon_twl WHERE gram = ?'
    anag_entries = c.execute(search_sql, (gram,))
    anag_entries = anag_entries.fetchall()
    return(anag_entries)


def search_blanag(gram):
    output = []
    numlt = len(gram)
    gram = gram.upper()
    gram = strsort(gram)
    nblk = gram.count('?')
    nv = multicount(gram, 'AEIOU')
    njqxz = multicount(gram, 'JQXZ')
    ntp = multicount(gram, 'BCFHKMPVWY') + njqxz
    pts = nv + multicount(gram, 'LNRST') + 2*multicount(gram, 'DG') +\
          3*multicount(gram, 'BCMP') + 4*multicount(gram, 'FHVWY') + 5*gram.count('K') +\
          8*multicount(gram, 'JX') + 10*multicount(gram,'QZ')
    search_sql = ''' SELECT * FROM lexicon_twl WHERE length = ? AND
                     vowels >= ? AND vowels <= ? AND
                     threeplus >= ? AND threeplus <= ? AND
                     score >= ? '''
    blanag_poss = c.execute(search_sql,
                            (numlt, nv, nv+nblk, ntp, ntp+nblk, pts+nblk))
    blanag_poss = blanag_poss.fetchall()
    for k in range(len(blanag_poss)):
        testcase = blanag_poss[k]
        gram_uniq = uniq_let(gram)
        add = True
        for ltr in gram_uniq:
            if testcase[0].count(ltr) < gram.count(ltr):
                add = False
                break
        if add:
            output.append(testcase)
    return(output)



# Trying to create a good search function.
# This first function is not intended to be used.
def search_list(searchlist):
    search_names = []
    for elt in searchlist:
        namecheck = elt.split(' ')
        search_names.append(namecheck[0])
    search_string = ''
    for k in range(len(searchlist)):
        if search_names[k] in ('length', 'score', 'vowels', 'jqxz', 'threeplus',\
                               'remfirst', 'remlist', 'fhook', 'bhook'):
            if k==0:
                search_string += searchlist[k]
            else:
                search_string += ' AND ' + searchlist[k]
    search_sql = 'SELECT * FROM lexicon_twl WHERE ' + search_string
    output_list = c.execute(search_sql)
    output_list = output_list.fetchall()
    return(output_list)
            

# This is the wrapper
def search_input():
    # This will be a function with different criteria that
    # Can be searched.
    print('You can select the following: minlength, maxlength,')
    print('vowels, jqxz, threeplus, points, includes, subgram.')
    print('Input "done" when you are finished.')
    print('Please specify a selection.')
    reply = ''
    replylist = []
    while reply != 'done':
        reply = input('? ')
        if reply != 'done':
            replylist.append(reply)
    outlist = search_list(replylist)
    return(outlist)

def search_subgram(gram, lengthmin, lengthmax):
    gram = gram.upper()
    gram_jqxz = multicount(gram, 'JQXZ')
    gram_scores = []
    for ltr in gram:
        gram_scores.append(pt_dic[ltr])
    gram_scores.sort()
    selected_cases = []
    for lgt in range(lengthmin, lengthmax+1):
        min_score = sum(gram_scores[:lgt])
        max_score = sum(gram_scores[-lgt:])
        search_sql = '''SELECT * FROM lexicon_twl WHERE
                        length = ? AND score >= ? AND score <= ?
                        AND jqxz <= ?'''
        first_list = c.execute(search_sql,
                                (lgt, min_score, max_score, gram_jqxz))
        first_list = first_list.fetchall()
        selected_cases.extend(first_list)
    output_list = []
    for data in selected_cases:
        include = True
        data_gram = data[0]
        dg_dic = let_dic(data_gram)
        gram_dic = let_dic(gram)
        dg_sum = 0
        for ltr in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if dg_dic[ltr] > gram_dic[ltr]:
                include = False
                break
            dg_sum += dg_dic[ltr]
        if dg_sum < len(data_gram):
            include = False
        if include:
            output_list.append(data)
    return(output_list)




# I am not sure if how much I want the list to be pared down
def save_entries(entrylist, name):
    prevgram = ''
    for k in range(len(entrylist)):
        gram = entrylist[k][0]
        add_sql = '''INSERT INTO gram_table(listname, gram)
                     VALUES(?,?)'''
        if gram != prevgram:
            c.execute(add_sql, (name, gram))
        prevgram = entrylist[k][0]
    conn.commit()

def save_grams(gramlist, name):
    for gram in gramlist:
        add_sql = '''INSERT INTO gram_table(listname, gram)
                     VALUES(?,?)'''
        c.execute(add_sql, (name, gram))
    conn.commit()


# Now I will add a few lists
add_list = False

if False:
    HighFive = search_list(['length = 5', 'score > 10'])
    HighSix = search_list(['length = 6', 'score > 14'])
    save_entries(HighFive, 'HighFive')
    save_entries(HighSix, 'HighSix')
    FiveVBingo = search_list(['length in (7,8)', 'vowels >= 5'])
    FourVSix = search_list(['length = 6', 'vowels >= 4'])
    FourVSeven = search_list(['length = 7', 'vowels = 4'])
    SixVNine = search_list(['length = 9', 'vowels >= 6'])
    save_entries(FiveVBingo, 'FiveVBingo')
    save_entries(FourVSix, 'FourVSix')
    save_entries(FourVSeven, 'FourVSeven')
    save_entries(SixVNine, 'SixVNine')

if add_list:
    DeregBingo = search_subgram('DEREGULATIONS', 7, 8)
    DeregNine = search_subgram('DEREGULATIONS', 9, 9)
    NarcoDeregBingo = search_subgram('NARCOTISEDEREGULATIONS', 7, 8)
    NarcoDeregNine = search_subgram('NARCOTISEDEREGULATIONS', 9, 9)
    save_entries(DeregBingo, 'DeregBingo')
    save_entries(DeregNine, 'DeregNine')
    save_entries(NarcoDeregBingo, 'NarcoDeregBingo')
    save_entries(NarcoDeregNine, 'NarcoDeregNine')
    conn.commit()







