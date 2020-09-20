import sqlite3

database = "Scrabble_Database.db"
conn = sqlite3.connect(database)

c = conn.cursor()

def gram_db(lexicon):
    gram_table_sql = 'CREATE TABLE IF NOT EXISTS gram_table_' + lexicon +\
                     '''(
                            listname text NOT NULL,
                            gram text NOT NULL
                        );'''
    c.execute(gram_table_sql)
    
    LPB_sql = 'SELECT * FROM lexicon_' + lexicon +\
              ' WHERE length > 6 AND length < 9 AND threeplus = 0'
    LPB_entries = c.execute(LPB_sql)
    LPB_entries = LPB_entries.fetchall()
    prevgram = ''
    for k in range(len(LPB_entries)):
        gram = LPB_entries[k][0]
        add_sql = 'INSERT INTO gram_table_' + lexicon +\
                  '''(listname, gram)
                     VALUES("LowPtBingo",?)'''
        if gram != prevgram:
            c.execute(add_sql, (LPB_entries[k][0],))
        prevgram = LPB_entries[k][0]
    conn.commit()


# Creating lists for hooks
def hook_db(lexicon):
    hook_table_sql = 'CREATE TABLE IF NOT EXISTS hook_table_'+ lexicon +\
                     '''(
                            listname text NOT NULL,
                            word text NOT NULL,
                            fhook text NOT NULL,
                            bhook text NOT NULL
                        );'''
    c.execute(hook_table_sql)
    
    manyhook_bingo_sql = 'SELECT * FROM lexicon_' + lexicon +\
                         ' WHERE length > 5 AND length < 9'
    manyhook_bingo_sql = c.execute(manyhook_bingo_sql)
    manyhook_bingo_sql = manyhook_bingo_sql.fetchall()
    for k in range(len(manyhook_bingo_sql)):
        fhook = manyhook_bingo_sql[k][9]
        bhook = manyhook_bingo_sql[k][10]
        if len(fhook) + len(bhook) > 4:
            add_sql = 'INSERT INTO hook_table_' + lexicon +\
                      '''(listname, word, fhook, bhook)
                         VALUES('ManyHook68', ?,?,?)'''
            c.execute(add_sql, (manyhook_bingo_sql[k][1], fhook, bhook))
    conn.commit()

# These functions are to be used internally
def alphasort(string):
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

# These functions are for users to call
def judge(string, lexicon):
    judgment = True
    string = string.upper()
    string = string.split(',')
    judgtuple = []
    for word in string:
        word = word.strip()
        judge_sql = 'SELECT * FROM lexicon_' + lexicon + ' WHERE word = ?'
        judge_entry = c.execute(judge_sql, (word,))
        judge_entry = judge_entry.fetchall()
        if len(judge_entry) == 0:
            judgment = False
            break
    return(judgment)


def search_anag(gram, lexicon, full_data = True):
    gram = gram.upper()
    gram = alphasort(gram)
    search_sql = 'SELECT * FROM lexicon_' + lexicon + ' WHERE gram = ?'
    anag_entries = c.execute(search_sql, (gram,))
    anag_entries = anag_entries.fetchall()
    if not full_data:
        for k in range(len(anag_entries)):
            anag_entries[k] = anag_entries[k][1]
    return(anag_entries)


def search_blanag(gram, lexicon, full_data = True):
    output = []
    numlt = len(gram)
    gram = gram.upper()
    gram = alphasort(gram)
    nblk = gram.count('?')
    nv = multicount(gram, 'AEIOU')
    njqxz = multicount(gram, 'JQXZ')
    ntp = multicount(gram, 'BCFHKMPVWY') + njqxz
    pts = nv + multicount(gram, 'LNRST') + 2*multicount(gram, 'DG') +\
          3*multicount(gram, 'BCMP') + 4*multicount(gram, 'FHVWY') + 5*gram.count('K') +\
          8*multicount(gram, 'JX') + 10*multicount(gram,'QZ')
    search_sql = 'SELECT * FROM lexicon_' + lexicon +\
                 ''' WHERE length = ? AND
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
            if full_data:
                output.append(testcase)
            else:
                output.append(testcase[1])
    return(output)



# Trying to create a good search function.
# This first function is not intended to be used.
def search_list(searchlist, lexicon):
    search_names = []
    for elt in searchlist:
        namecheck = elt.split(' ')
        search_names.append(namecheck[0])
    search_string = ''
    for k in range(len(searchlist)):
        if search_names[k] in ('length', 'score', 'vowels', 'jqxz', 'threeplus',\
                               'remfirst', 'remlist', 'fhook', 'bhook',\
                               'nrack', 'nrack_adj'):
            if k==0:
                search_string += searchlist[k]
            else:
                search_string += ' AND ' + searchlist[k]
    search_sql = 'SELECT * FROM lexicon_' + lexicon + ' WHERE ' + search_string
    output_list = c.execute(search_sql)
    output_list = output_list.fetchall()
    return(output_list)
            

# This is the wrapper
def search_input(lexicon):
    # This will be a function with different criteria that
    # Can be searched.
    print('You can select the following characteristics:')
    print('minlength, maxlength, vowels, jqxz, threeplus,')
    print('points, includes, subgram, nrack, nrack_adj.')
    print('Please include a space after each characteristic.')
    print('Input "done" when you are finished.')
    print('Please specify a selection.')
    reply = ''
    replylist = []
    while reply != 'done':
        reply = input('? ')
        if reply != 'done':
            replylist.append(reply)
    outlist = search_list(replylist, lexicon = lexicon)
    return(outlist)

def search_subgram(gram, lengthmin, lengthmax, lexicon, full_data = True):
    gram = gram.upper()
    nb = gram.count('?')
    gram_jqxz = multicount(gram, 'JQXZ') + nb
    gram_scores = []
    for ltr in gram:
        gram_scores.append(pt_dic[ltr])
    gram_scores.sort()
    selected_cases = []
    for lgt in range(lengthmin, lengthmax+1):
        min_score = sum(gram_scores[:lgt]) + nb
        max_score = sum(gram_scores[-lgt:]) + 10*nb
        search_sql = 'SELECT * FROM lexicon_' + lexicon +\
                     '''WHERE length = ? AND score >= ? AND
                        score <= ? AND jqxz <= ?'''
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
        blank_used = 0
        for ltr in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if dg_dic[ltr] > gram_dic[ltr]:
                if dg_dic[ltr] > gram_dic[ltr] + nb - blank_used:
                    include = False
                    break
                else:
                    blank_used += dg_dic[ltr] - gram_dic[ltr]
            dg_sum += dg_dic[ltr]
        if dg_sum < len(data_gram):
            include = False
        if include:
            if full_data:
                output_list.append(data)
            else:
                output.append(data[1])
    return(output_list)




# I am not sure if how much I want the list to be pared down
def save_entries(entrylist, name, lexicon):
    prevgram = ''
    for k in range(len(entrylist)):
        gram = entrylist[k][0]
        add_sql = 'INSERT INTO gram_table_' + lexicon +\
                  '''(listname, gram)
                     VALUES(?,?)'''
        if gram != prevgram:
            c.execute(add_sql, (name, gram))
        prevgram = entrylist[k][0]
    conn.commit()

def save_grams(gramlist, name, lexicon):
    for gram in gramlist:
        add_sql = 'INSERT INTO gram_table_' + lexicon +\
                  '''(listname, gram)
                     VALUES(?,?)'''
        c.execute(add_sql, (name, gram))
    conn.commit()



# Now I will add a few lists for examples
add_list = False

if add_list:
    DeregBingo_nwl18 = search_subgram('DEREGULATIONS', 7, 8, lexicon = 'nwl18')
    DeregNine_nwl18 = search_subgram('DEREGULATIONS', 9, 9, lexicon = 'nwl18')
    HighFive_nwl18 = search_list(['length = 5', 'score > 10'], lexicon = 'nwl18')
    save_entries(DeregBingo_nwl18, 'DeregBingo', lexicon = 'nwl18')
    save_entries(DeregNine_nwl18, 'DeregNine', lexicon = 'nwl18')
    save_entries(HighFive_nwl18, 'HighFive', lexicon = 'nwl18')
    conn.commit()
