import sqlite3
import random as r
import string

def db_creator(filename):
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

def db_connector(filename):
    try:
        conn = sqlite3.connect(filename)
        print(conn)
    except sqlite3.Error as e:
        print(e)
    
    return(None)

def drop_table(conn, table_drop_sql):
    try:
        c = conn.cursor()
        c.execute(table_drop_sql)
    except sqlite3.Error as e:
        print(e)

def create_table(conn, create_table_sql):
    # Adapted from a sqlite tutorial.
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def my_cumsum(list):
    output = [list[0]]
    for k in range(1,len(list)):
        output.append(output[-1] + list[k])
    return(output)

def resort(word, ltrord):
    list = []
    for ltr in word:
        list.append(ltrord.index(ltr))
    list.sort()
    output = ''
    for elt in list:
        output = output + ltrord[elt]
    return(output)

# Connecting to a database
database = "Scrabble_Database.db"
conn = sqlite3.connect(database)

# Functions to create a table for anagram quizzes.
def quiz_anag_db_drop(lexicon):
    drop_table(conn, 'DROP TABLE IF EXISTS quiz_anag_' + lexicon)
    
def quiz_anag_db(lexicon):
    sql_create = 'CREATE TABLE IF NOT EXISTS quiz_anag_' + lexicon +\
                 '''(   
                        user text NOT NULL,
                        gram text NOT NULL,
                        answers text,
                        num_cor integer,
                        num_inc integer,
                        wt_cor double,
                        wt_inc double,
                        prob_val double,
                        FOREIGN KEY (user) REFERENCES users (user)
                    );'''
    create_table(conn, sql_create)
    conn.commit

def quiz_anag_bilex_db(lex1, lex2):
    sql_create = 'CREATE TABLE IF NOT EXISTS quiz_anag_' + lex1+'_'+lex2 +\
                 '''(   
                        user text NOT NULL,
                        gram text NOT NULL,
                        answers1 text,
                        answers2 text,
                        num_cor integer,
                        num_inc integer,
                        wt_cor double,
                        wt_inc double,
                        prob_val double,
                        FOREIGN KEY (user) REFERENCES users (user)
                    );'''
    create_table(conn, sql_create)
    conn.commit

# Table for hook quizzes
def quiz_hook_db_drop(lexicon):
    drop_table(conn, 'DROP TABLE IF EXISTS quiz_hook_' + lexicon)

def quiz_hook_db(lexicon):
    sql_create = 'CREATE TABLE IF NOT EXISTS quiz_hook_' + lexicon +\
                  '''(
                         user text NOT NULL,
                         word text NOT NULL,
                         fhook text,
                         bhook text,
                         num_cor integer,
                         num_inc integer,
                         wt_cor double,
                         wt_inc double,
                         prob_val double,
                         FOREIGN KEY (user) REFERENCES users (user)
                     );'''
    create_table(conn, sql_create)
    conn.commit()

def quiz_hook_bilex_db(lex1, lex2):
    sql_create = 'CREATE TABLE IF NOT EXISTS quiz_hook_' + lex1+'_'+lex2 +\
                  '''(
                         user text NOT NULL,
                         word text NOT NULL,
                         fhook1 text,
                         fhook2 text,
                         bhook1 text,
                         bhook2 text,
                         num_cor integer,
                         num_inc integer,
                         wt_cor double,
                         wt_inc double,
                         prob_val double,
                         FOREIGN KEY (user) REFERENCES users (user)
                     );'''
    create_table(conn, sql_create)
    conn.commit()

# A function to check letter order
def ltrord_check(ltrord):
    ltrord = ltrord.upper()
    ltrord_length = True
    ltrord_inclall = True
    if len(ltrord) != 26:
        ltrord_length = False
    for ltr in string.ascii_uppercase:
        if ltr not in ltrord:
            ltrord_inclall = False
            break
    ltrord_legal = ltrord_length and ltrord_inclall
    return(ltrord_legal)

# To create users, if desired
def create_user(username, ltrorder, multiplier,
               lexicon = None, lex1 = None, lex2 = None):
    """
    Creating a new user
    """
    sql = ''' INSERT INTO users(user, letterorder, multiplier,
                                lexicon, lex1, lex2)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    ltrorder = letrorder.upper()
    if not ltrord_check(ltrorder):
        raise ValueError('Not a legal letter order!')
    userrow = (username, ltrorder, multiplier,\
               lexicon, lex1, lex2)
    cur.execute(sql, userrow)
    return(cur.lastrowid)

def extract_list(lname, lexicon):
    c = conn.cursor()
    outlist = c.execute('SELECT * FROM gram_table_' + lexicon + ' WHERE listname = ?', (lname,))
    outlist = outlist.fetchall()
    output = []
    for k in range(len(outlist)):
        output.append(outlist[k][1])
    return(output)


### Creating an opportunity to login:
def login_fxn():
    uname_global = None
    login_code = False
    while(login_code == False):
        login = input('Would you like to login (y/n)?: ')
        if login.lower() == 'y':
            uname_global = input('Username: ')
            login_code = True
            usrupd_code = input('Would you like to update defaults (y/n)?: ')
            # If you would want to update information on the defaults.
            if usrupd_code.lower() == 'y':
                lex_code = input('Update lexica (y/n)?: ')
                if lex_code.lower() == 'y':
                    lexicon_new = input('Preferred lexicon for unilexical quizzes: ')
                    lexicon_new = lexicon_new.strip(' ')
                    bilex_new = input('Bilex lexicon order: ')
                    bilex_new = bilex_new.split(',')
                    lex1_new = bilex_new[0].strip()
                    lex2_new = bilex_new[1].strip()
                    sql = 'UPDATE users SET lexicon = ?, lex1 = ?, lex2 = ? WHERE user = ?'
                    c.execute(sql, (lexicon_new, lex1_new, lex2_new, uname_global))
                    conn.commit()
                ltrord_code = input('Update letter order (y/n)?: ')
                if ltrord_code.lower() == 'y':
                    ltrord_legal = False
                    while not ltrord_legal:
                        ltrord_new = input('New letter order (type "n" to cancel): ')
                        ltrord_new = ltrord.upper()
                        if ltrord_new == 'n':
                            sql = 'SELECT letterorder FROM users WHERE user == ?'
                            ltrord_new = c.execute(sql, (uname_global,))
                        ltrord_legal = ltrord_check(ltrord_new)
                        if not ltrord_legal:
                            print('Illegal letter order. Try again.')
                    sql = 'UPDATE users SET letterorder = ? WHERE user = ?'
                    c.execute(sql, (ltrord_new, uname_global))
                    conn.commit()
                mult_code = input('Update multiplier (y/n)?: ')
                if mult_code.lower() == 'y':
                    mult_new = input('New multiplier: ')
                    while (mult_new < 1) or (mult_new > 2):
                        print('You chose a weird multiplier value.')
                        mult_check = input('Are you sure about that number (y/n)?: ')
                        if mult_check.lower() == 'y':
                            pass
                        elif mult_check.lower() == 'n':
                            mult_new = input('New multiplier: ')
                        else:
                            print('Not "y" or "n". Try again.')
                    sql = 'UPDATE users SET multiplier = ? WHERE user = ?'
                    c.execute(sql, (mult_new, uname_global))
                    conn.commit()
        
        elif login.lower() == 'n':
            print('You did not log in. Noted.')
            login_code = True
        else:
            print('Not "y" or "n". Try again.')
    return(uname_global)

uname_global = login_fxn()

# Creating a function for anagram quizzes
# You can either use a list, saved as a python list
# ... or a names of a word list from `gram_table`
def quiz_anag(gramlist, userid = uname_global, lexicon = None, listname = True):
    
    # Starting the cursor
    c = conn.cursor()
    
    # Using default lexicon if unspecified
    if lexicon == None:
        sql = 'SELECT lexicon FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexicon = usr_lex[0][0]
        print(lexicon)
    
    # It could be good to do multiple lists at the same time.
    if listname:
        gramlist = extract_list(gramlist, lexicon)
    
    print('You are quizzing!')   
    
    # Using the user specified letter order and multiplier
    userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    userdata = userdata.fetchall()
    ltrord = userdata[0][1]
    multiplier = userdata[0][2]
    
    k = 0
    # I would like to do this without a 'for' loop.
    qa_entries = []
    for k in range(len(gramlist)):
        sql_search_qa = 'SELECT * FROM quiz_anag_' + lexicon +\
                        ' WHERE gram = ? AND user = ?'
        curr_entry = c.execute(sql_search_qa, (gramlist[k], userid))
        curr_entry = curr_entry.fetchall()
        #print(str(k), curr_entry)
        if len(curr_entry) > 0:
            qa_entries.extend(curr_entry)
    
    k = 0
    prb_list = []
    for k in range(len(qa_entries)):
        prb_list.append(qa_entries[k][7])
        if qa_entries[k][1] in gramlist:
            gramlist.remove(qa_entries[k][1])
    
    # Now I will search the dictionary for any new information
    if len(gramlist) > 0:
        print(len(gramlist))
        lex_entries = []
        for k in range(len(gramlist)):
            #print(gramlist[k])
            sql_search_lex = 'SELECT * FROM lexicon_' + lexicon + ' WHERE gram = ?'
            curr_entry = c.execute(sql_search_lex, (gramlist[k],))
            lex_entries.extend(curr_entry.fetchall())
            #if len(lex_entries) > 0:
                #print(len(lex_entries), lex_entries[-1])
        
        gramprev = ''
        answers = ''
        for k in range(len(lex_entries)):
            gram = lex_entries[k][0]
            if k > 0 and gram != gramprev:
                if answers == '':
                    print(k)
                    print(gramprev)
                    break
                sql = 'INSERT INTO quiz_anag_' + lexicon +\
                      '''(user,gram,answers,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                         VALUES(?,?,?,?,?,?,?,?)'''
                c.execute(sql, (userid, gramprev, answers, 0,0,0,0,5))
                qa_entries.append((userid, gramprev, answers, 0,0,0,0,5))
                prb_list.append(5)
            if gram != gramprev:
                answers = lex_entries[k][1]
                try:
                    gramlist.remove(gramprev)
                except ValueError:
                    print(gramprev)
            else:
                answers = answers + '_' + lex_entries[k][1]
            gramprev = lex_entries[k][0]
        
        sql = 'INSERT INTO quiz_anag_' + lexicon +\
              '''(user,gram,answers,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                 VALUES(?,?,?,?,?,?,?,?)'''
        c.execute(sql, (userid, gramprev, answers, 0,0,0,0,5))
        qa_entries.append((userid, gramprev, answers, 0,0,0,0,5))
        prb_list.append(5)
        try:
            gramlist.remove(gramprev)
        except ValueError:
            print(gramprev)
    conn.commit()
    
    # If anything is left, it has no anagrams
    if len(gramlist) > 0:
        for gram in gramlist:
            sql = 'INSERT INTO quiz_anag_' + lexicon +\
                  '''(user,gram,answers,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                     VALUES(?,?,?,?,?,?,?,?)'''
            c.execute(sql, (userid, gram, '', 0,0,0,0,5))
            qa_entries.append((userid, gram, '', 0,0,0,0,5))
            prb_list.append(5)
    conn.commit()
    
    # Now we will begin the quizzing
    quiz = True
    qatt = 0
    qcor = 0
    while quiz:
        # numpy was hard to install on linux, so I didn't use it
        prb_cumsum = my_cumsum(prb_list)
        pick = r.random()*prb_cumsum[-1]
        k = 0
        while pick > prb_cumsum[k]:
            k += 1
        question = resort(qa_entries[k][1], ltrord)
        answers = qa_entries[k][2].split('_')
        answers.sort()
        endq = False
        print(question)
        replylist = []
        while not endq:
            reply = input('? ')
            reply = reply.upper()
            if reply == '' or reply == 'Q':
                endq = True
                if reply == 'Q':
                    quiz = False
            else:
                replylist.append(reply)
        replylist.sort()
        print(answers)
        print(replylist)
        answer_data= []
        for word in answers:
            sql = '''SELECT fhook, remfirst, word, remlast, bhook
                     FROM lexicon_''' + lexicon + ' WHERE word = ?'
            word_props = c.execute(sql, (word,))
            word_props = word_props.fetchall()
            answer_data.append(word_props)
        for datum in answer_data:
            print(datum)
        qatt += 1
        if replylist == answers:
            qcor += 1
            new_cor = qa_entries[k][3] + 1
            new_inc = qa_entries[k][4]
            natt = new_cor + new_inc
            # This next line could be changed
            # To allow for a user specific number
            # Controls the weighting of more recent responses
            new_wt_cor = qa_entries[k][5] + multiplier
            new_wt_cor *= natt/(natt+multiplier-1)
            new_wt_inc = qa_entries[k][6]*natt/(natt+multiplier-1)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qa_entries[k] = (qa_entries[k][0], qa_entries[k][1], qa_entries[k][2],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob) 
        else:
            new_cor = qa_entries[k][3]
            new_inc = qa_entries[k][4] + 1
            natt = new_cor + new_inc
            # This next line could be changed
            # To allow for a user specific number
            new_wt_inc = qa_entries[k][6] + multiplier
            new_wt_inc *= natt/(natt+multiplier-1)
            new_wt_cor = qa_entries[k][5]*natt/(natt+multiplier-1)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qa_entries[k] = (qa_entries[k][0], qa_entries[k][1], qa_entries[k][2],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob)
        print(str(new_cor) + '/' + str(new_cor+new_inc) + ' ' +\
              str(round(new_prob,2)))
        # Updating the database
        sql = 'UPDATE quiz_anag_' + lexicon +\
              ''' SET num_cor = ?,
                      num_inc = ?,
                      wt_cor = ?,
                      wt_inc = ?,
                      prob_val = ?
                  WHERE gram = ?'''
        c.execute(sql, (qa_entries[k][3],\
                        qa_entries[k][4],\
                        qa_entries[k][5],\
                        qa_entries[k][6],\
                        qa_entries[k][7],\
                        qa_entries[k][1]))
        conn.commit()
        # Updating probabilities
        prb_list[k] = qa_entries[k][7]
    
    # Displaying statistics
    print('Questions Correct:   ' + str(qcor) + '\n')
    print('Questions Attempted: ' + str(qatt) + '\n')
    print('Thanks for quizzing!')


# Hook quiz using databases
def extract_hook(lname, lexicon):
    c = conn.cursor()
    outlist = c.execute('SELECT * FROM hook_table_' + lexicon + \
                        ' WHERE listname = ?', (lname,))
    outlist = outlist.fetchall()
    output = []
    for k in range(len(outlist)):
        output.append(outlist[k][1])
    return(output)

def quiz_hook(list_len, userid = uname_global, lexicon = None, listname = True):
    hooklist = []
    c = conn.cursor()
    
    # Using default lexicon if unspecified
    if lexicon == None:
        sql = 'SELECT lexicon FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexicon = usr_lex[0][0]
        print(lexicon)
    
    # It could be good to do multiple lists at the same time.
    if str(type(list_len)) == "<class 'int'>":
        hookcheck = 'SELECT * FROM lexicon_' + lexicon + ' WHERE length = ?'
        datalist = c.execute(hookcheck, (list_len,))
        datalist = datalist.fetchall()
        for data in datalist:
            hooklist.append(data[1])
    
    if str(type(list_len)) == "<class 'str'>":   
        if listname:
            hooklist = extract_hook(list_len, lexicon)
    
    # Adding entries to quiz_hook if necessary.
    for word in hooklist:
        hookcheck = 'SELECT * FROM quiz_hook_' + lexicon + ' WHERE word = ?'
        hookcheck = c.execute(hookcheck, (word,))
        hookcheck = hookcheck.fetchall()
        if len(hookcheck) == 0:
            adddata = 'SELECT * FROM lexicon_' + lexicon + ' WHERE word = ?'
            adddata = c.execute(adddata, (word,))
            adddata = adddata.fetchall()
            hookadd = 'INSERT INTO quiz_hook_' + lexicon +\
                      '''(user, word, fhook, bhook,
                                               num_cor, num_inc, wt_cor, wt_inc,
                                               prob_val)
                         VALUES(?,?,?,?,?,?,?,?,?)'''
            c.execute(hookadd, (userid, word, adddata[0][9], adddata[0][10],\
                                0,0,0,0,5))
            conn.commit()
    
    print('You are quizzing!')   
    
    # Using the user specified letter order and multiplier
    userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    userdata = userdata.fetchall()
    ltrord = userdata[0][1]
    multiplier = userdata[0][2]
    
    k = 0
    # I would like to do this without a 'for' loop.
    qh_entries = []
    for k in range(len(hooklist)):
        sql_search_qh = 'SELECT * FROM quiz_hook_' + lexicon + \
                        ' WHERE word = ? AND user = ?'
        curr_entry = c.execute(sql_search_qh, (hooklist[k], userid))
        curr_entry = curr_entry.fetchall()
        qh_entries.append(curr_entry[0])
    
    k = 0
    prb_list = []
    for k in range(len(qh_entries)):
        prb_list.append(qh_entries[k][8])
    
    # Now we will begin the quizzing
    quiz = True
    qatt = 0
    qcor = 0
    while quiz:
        # numpy was hard to install on linux, so I didn't use it
        prb_cumsum = my_cumsum(prb_list)
        pick = r.random()*prb_cumsum[-1]
        k = 0
        while pick > prb_cumsum[k]:
            k += 1
        question = qh_entries[k][1]
        fhook = resort(qh_entries[k][2], ltrord)
        bhook = resort(qh_entries[k][3], ltrord)
        endq = False
        print(question)
        replylist = []
        fhook_ans = input('Front Hooks? ')
        fhook_ans = fhook_ans.upper()
        fhook_ans = resort(fhook_ans, ltrord)
        bhook_ans = input('Back Hooks? ')
        bhook_ans = bhook_ans.upper()
        bhook_ans = resort(bhook_ans, ltrord)
        if fhook_ans == 'Q' and bhook_ans == 'Q':
            quiz = False
        replylist.sort()
        print('Front Hooks:')
        print(fhook)
        print(fhook_ans)
        print('Back Hooks:')
        print(bhook)
        print(bhook_ans)
        
        answers = []
        for ltr in fhook:
            answers.append(ltr + question)
        for ltr in bhook:
            answers.append(question + ltr)
        
        answer_data = []
        for word in answers:
            sql = 'SELECT fhook, remfirst, word, remlast, bhook FROM lexicon_' + \
                  lexicon + ' WHERE word = ?'
            word_props = c.execute(sql, (word,))
            word_props = word_props.fetchall()
            answer_data.append(word_props)
        for datum in answer_data:
            print(datum)
        if quiz:
            qatt += 1
            if fhook_ans == fhook and bhook_ans == bhook:
                qcor += 1
                new_cor = qh_entries[k][4] + 1
                new_inc = qh_entries[k][5]
                natt = new_cor + new_inc
                # This next line could be changed
                # To allow for a user specific number
                # Controls the weighting of more recent responses
                new_wt_cor = qh_entries[k][6] + multiplier
                new_wt_cor *= natt/(natt+multiplier - 1)
                new_wt_inc = qh_entries[k][7]*natt/(natt+multiplier - 1)
                if new_wt_inc >= new_wt_cor:
                    new_prob = 1+new_wt_inc-new_wt_cor
                else:
                    new_prob = 1/(1+new_wt_cor-new_wt_inc)
                qh_entries[k] = (qh_entries[k][0], qh_entries[k][1],\
                                 qh_entries[k][2], qh_entries[k][3],\
                                 new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob) 
            else:
                new_cor = qh_entries[k][4]
                new_inc = qh_entries[k][5] + 1
                natt = new_cor + new_inc
                # This next line could be changed
                # To allow for a user specific number
                new_wt_inc = qh_entries[k][7] + multiplier
                new_wt_inc *= natt/(natt+multiplier-1)
                new_wt_cor = qh_entries[k][6]*natt/(natt+multiplier-1)
                if new_wt_inc >= new_wt_cor:
                    new_prob = 1+new_wt_inc-new_wt_cor
                else:
                    new_prob = 1/(1+new_wt_cor-new_wt_inc)
                qh_entries[k] = (qh_entries[k][0], qh_entries[k][1],\
                                 qh_entries[k][2], qh_entries[k][3],\
                                 new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob)
            print(str(new_cor) + '/' + str(new_cor+new_inc) + ' ' +\
                  str(round(new_prob,2)))
            # Updating the database
            sql = 'UPDATE quiz_hook_' + lexicon +\
                  ''' SET num_cor = ?,
                          num_inc = ?,
                          wt_cor = ?,
                          wt_inc = ?,
                          prob_val = ?
                      WHERE word = ?'''
            c.execute(sql, (qh_entries[k][4],\
                            qh_entries[k][5],\
                            qh_entries[k][6],\
                            qh_entries[k][7],\
                            qh_entries[k][8],\
                            qh_entries[k][1]))
            conn.commit()
            # Updating probabilities
            prb_list[k] = qh_entries[k][8]
    
    # Displaying statistics
    print('Questions Correct:   ' + str(qcor) + '\n')
    print('Questions Attempted: ' + str(qatt) + '\n')
    print('Thanks for quizzing!')



# Now I am editing these functions to be bilexical!
def quiz_anag_bilex(gramlist, userid = uname_global, lex1 = None, lex2 = None,
                    listname = True, lex_subset = False):
    # This quiz will be bilexical
    # If lex_subset = True, then it will assume that lex2
    # ... is a subset of lex1.
    c = conn.cursor()
    
    # Using default lexica if unspecified
    if lex1 == None:
        sql = 'SELECT lex1 FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexicon = usr_lex[0][0]
        print('lex1 = ' + lex1)
    if lex2 == None:
        sql = 'SELECT lex2 FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lex2 = usr_lex[0][0]
        print('lex2 = ' + lex2)
    
    # It could be good to do multiple lists at the same time.
    if listname:
        gramlist1 = extract_list(gramlist, lex1)
        gramlist2 = extract_list(gramlist, lex2)
    # Combining into 1.
    gramlist = list(set(gramlist1) | set(gramlist2))
    
    print('You are quizzing!')   
    
    # Using the user specified letter order and multiplier
    userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    userdata = userdata.fetchall()
    ltrord = userdata[0][1]
    multiplier = userdata[0][2]
    
    k = 0
    # Incorporating elements previously in the quiz_anag table
    qa_entries = []
    for k in range(len(gramlist)):
        sql_search_qa = 'SELECT * FROM quiz_anag_' + lex1+'_'+lex2 +\
                        ' WHERE gram = ? AND user = ?'
        curr_entry = c.execute(sql_search_qa, (gramlist[k], userid))
        curr_entry = curr_entry.fetchall()
        #print(str(k), curr_entry)
        if len(curr_entry) > 0:
            qa_entries.extend(curr_entry)
    
    # Adding the proportional probability terms
    k = 0
    prb_list = []
    for k in range(len(qa_entries)):
        prb_list.append(qa_entries[k][8])
        if qa_entries[k][1] in gramlist:
            gramlist.remove(qa_entries[k][1])
            try:
                gramlist1.remove(qa_entries[k][1])
            except ValueError:
                pass
            try:
                gramlist2.remove(qa_entries[k][1])
            except ValueError:
                pass
    
    # Now I will search the dictionary for any new information
    if len(gramlist) > 0:
        print(len(gramlist))
        lex_answers = []
        for k in range(len(gramlist)):
            # lexicon 1
            sql_search_lex = 'SELECT * FROM lexicon_' + lex1 + ' WHERE gram = ?'
            curr_entries = c.execute(sql_search_lex, (gramlist[k],))
            curr_entries = curr_entries.fetchall()
            new_answer1 = ''
            for ell in range(len(curr_entries)):
                if ell > 0:
                    new_answer1 += '_'
                new_answer1 += curr_entries[ell][1]
            # lexicon 2
            sql_search_lex = 'SELECT * FROM lexicon_' + lex2 + ' WHERE gram = ?'
            curr_entries = c.execute(sql_search_lex, (gramlist[k],))
            curr_entries = curr_entries.fetchall()
            new_answer2 = ''
            for ell in range(len(curr_entries)):
                if ell > 0:
                    new_answer2 += '_'
                new_answer2 += curr_entries[ell][1]
            # Appending results
            lex_answers.append([gramlist[k], new_answer1, new_answer2])
        
        
        for k in range(len(lex_answers)):
            sql = 'INSERT INTO quiz_anag_' + lex1+'_'+lex2 +\
                  '''(user,gram,answers1,answers2,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                     VALUES(?,?,?,?,?,?,?,?,?)'''
            c.execute(sql, (userid, lex_answers[k][0], lex_answers[k][1],\
                               lex_answers[k][2], 0,0,0,0,5))
            qa_entries.append((userid, lex_answers[k][0], lex_answers[k][1],\
                               lex_answers[k][2], 0,0,0,0,5))
            prb_list.append(5)
        
            try:
                    gramlist.remove(lex_answers[k][0])
            except ValueError:
                print(lex_answers[k][0])
            try:
                gramlist1.remove(lex_answers[k][0])
            except ValueError:
                pass
            try:
                gramlist2.remove(lex_answers[k][0])
            except ValueError:
                pass
    conn.commit()
    
    # If anything is left, it has no anagrams
    if len(gramlist) > 0:
        for gram in gramlist:
            sql = 'INSERT INTO quiz_anag_' + lex1+'_'+lex2 +\
                  '''(user,gram,answers1,answers2,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                     VALUES(?,?,?,?,?,?,?,?,?)'''
            c.execute(sql, (userid, gram, '', '', 0,0,0,0,5))
            qa_entries.append((userid, gram, '', '', 0,0,0,0,5))
            prb_list.append(5)
    conn.commit()
    
    # Now we will begin the quizzing
    quiz = True
    qatt = 0
    qcor = 0
    while quiz:
        # numpy was hard to install on linux, so I didn't use it
        prb_cumsum = my_cumsum(prb_list)
        pick = r.random()*prb_cumsum[-1]
        k = 0
        while pick > prb_cumsum[k]:
            k += 1
        question = resort(qa_entries[k][1], ltrord)
        answers1 = qa_entries[k][2].split('_')
        answers2 = qa_entries[k][3].split('_')
        ans_1 = list(set(answers1) - set(answers2))
        ans_2 = list(set(answers2) - set(answers1))
        ans_3 = list(set(answers1) & set(answers2))
        # Sorting answers
        if ans_1 == ['']:
            ans_1 = []
        if ans_2 == ['']:
            ans_2 = []
        if ans_3 == ['']:
            ans_3 = []
        ans_1.sort()
        ans_3.sort()
        # ans_2 will be sorted later
        endq = False
        print(question)
        print(lex1 + ' only')
        replylist1 = []
        while not endq:
            reply = input('? ')
            reply = reply.upper()
            if reply == '' or reply == 'Q':
                endq = True
                if reply == 'Q':
                    quiz = False
            else:
                replylist1.append(reply)
        replylist1.sort()
        
        endq = False
        replylist2 = []
        if not lex_subset:
            ans_2.sort()
            print(lex2 + ' only')
            while not endq:
                reply = input('? ')
                reply = reply.upper()
                if reply == '' or reply == 'Q':
                    endq = True
                    if reply == 'Q':
                        quiz = False
                else:
                    replylist2.append(reply)
            replylist2.sort()
        else:
            ans_2 = []
        print('both ' + lex1 + ' and ' + lex2)
        
        endq = False
        replylist3 = []
        while not endq:
            reply = input('? ')
            reply = reply.upper()
            if reply == '' or reply == 'Q':
                endq = True
                if reply == 'Q':
                    quiz = False
            else:
                replylist3.append(reply)
        replylist3.sort()
        # In this case, I do not show the users answers again.
        print(ans_1)
        if not lex_subset:
            print(ans_2)
        print(ans_3)
        answer_data = []
        # I do not show data about the answers here
        # ... for now.
        qatt += 1
        if replylist1 == ans_1 and replylist3 == ans_3 and \
           replylist2 == ans_2:
            qcor += 1
            new_cor = qa_entries[k][4] + 1
            new_inc = qa_entries[k][5]
            natt = new_cor + new_inc
            # This next line could be changed
            # To allow for a user specific number
            # Controls the weighting of more recent responses
            new_wt_cor = qa_entries[k][6] + multiplier
            new_wt_cor *= natt/(natt+multiplier-1)
            new_wt_inc = qa_entries[k][7]*natt/(natt+multiplier-1)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qa_entries[k] = (qa_entries[k][0], qa_entries[k][1],\
                             qa_entries[k][2], qa_entries[k][3],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob) 
        else:
            new_cor = qa_entries[k][4]
            new_inc = qa_entries[k][5] + 1
            natt = new_cor + new_inc
            # This next line could be changed
            # To allow for a user specific number
            new_wt_inc = qa_entries[k][7] + multiplier
            new_wt_inc *= natt/(natt+multiplier-1)
            new_wt_cor = qa_entries[k][6]*natt/(natt+multiplier-1)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qa_entries[k] = (qa_entries[k][0], qa_entries[k][1],\
                             qa_entries[k][2], qa_entries[k][3],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob)
        print(str(new_cor) + '/' + str(new_cor+new_inc) + ' ' +\
              str(round(new_prob,2)))
        # Updating the database
        sql = 'UPDATE quiz_anag_' + lex1+'_'+lex2 +\
              ''' SET num_cor = ?,
                      num_inc = ?,
                      wt_cor = ?,
                      wt_inc = ?,
                      prob_val = ?
                  WHERE gram = ?'''
        c.execute(sql, (qa_entries[k][4],\
                        qa_entries[k][5],\
                        qa_entries[k][6],\
                        qa_entries[k][7],\
                        qa_entries[k][8],\
                        qa_entries[k][1]))
        conn.commit()
        # Updating probabilities
        prb_list[k] = qa_entries[k][8]
    
    # Displaying statistics
    print('Questions Correct:   ' + str(qcor) + '\n')
    print('Questions Attempted: ' + str(qatt) + '\n')
    print('Thanks for quizzing!')


def quiz_hook_bilex(list_len, userid = uname_global, lex1 = None, lex2 = None,\
                    listname = True, lex_subset = True):
    hooklist = []
    c = conn.cursor()
    
    # Using default lexica if unspecified
    if lex1 == None:
        sql = 'SELECT lex1 FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexicon = usr_lex[0][0]
        print('lex1 = ' + lex1)
    if lex2 == None:
        sql = 'SELECT lex2 FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lex2 = usr_lex[0][0]
        print('lex2 = ' + lex2)
    
    # It could be good to do multiple lists at the same time.
    if str(type(list_len)) == "<class 'int'>":
        hookcheck = 'SELECT * FROM lexicon_' + lex1 + ' WHERE length = ?'
        datalist = c.execute(hookcheck, (list_len,))
        datalist = datalist.fetchall()
        hookcheck = 'SELECT * FROM lexicon_' + lex2 + ' WHERE length = ?'
        datalist2 = c.execute(hookcheck, (list_len,))
        datalist2 = datalist2.fetchall()
        datalist.extend(datalist2)
        for data in datalist:
            hooklist.append(data[1])
        hooklist = list(set(hooklist))
    
    if str(type(list_len)) == "<class 'str'>":   
        if listname:
            hooklist = extract_hook(list_len, lexicon)
    
    # Adding entries to quiz_hook if necessary.
    for word in hooklist:
        hookcheck = 'SELECT * FROM quiz_hook_' + lex1+'_'+lex2 + ' WHERE word = ?'
        hookcheck = c.execute(hookcheck, (word,))
        hookcheck = hookcheck.fetchall()
        if len(hookcheck) == 0:
            adddata1 = 'SELECT * FROM lexicon_' + lex1 + ' WHERE word = ?'
            adddata1 = c.execute(adddata1, (word,))
            adddata1 = adddata1.fetchall()
            adddata2 = 'SELECT * FROM lexicon_' + lex2 + ' WHERE word = ?'
            adddata2 = c.execute(adddata2, (word,))
            adddata2 = adddata2.fetchall()
            if len(adddata1) > 0 and len(adddata2) > 0:
                hookadd = 'INSERT INTO quiz_hook_' + lex1+'_'+lex2 +\
                          '''(user, word, fhook1, fhook2, bhook1, bhook2,
                                                   num_cor, num_inc, wt_cor, wt_inc,
                                                   prob_val)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
                c.execute(hookadd, (userid, word, adddata1[0][9], adddata2[0][9],\
                                    adddata1[0][10], adddata2[0][10],\
                                    0,0,0,0,5))
            elif len(adddata1) > 0 and len(adddata2) == 0:
                hookadd = 'INSERT INTO quiz_hook_' + lex1+'_'+lex2 +\
                          '''(user, word, fhook1, fhook2, bhook1, bhook2,
                                                   num_cor, num_inc, wt_cor, wt_inc,
                                                   prob_val)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
                c.execute(hookadd, (userid, word, adddata1[0][9], '',\
                                    adddata1[0][10], '',\
                                    0,0,0,0,5))
            elif len(adddata1) == 0 and len(adddata2) > 0:
                hookadd = 'INSERT INTO quiz_hook_' + lex1+'_'+lex2 +\
                          '''(user, word, fhook1, fhook2, bhook1, bhook2,
                                                   num_cor, num_inc, wt_cor, wt_inc,
                                                   prob_val)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?)'''
                c.execute(hookadd, (userid, word, '', adddata2[0][9],\
                                    '', adddata2[0][10],\
                                    0,0,0,0,5))
            conn.commit()
    
    print('You are quizzing!')   
    
    # Using the user specified letter order and multiplier
    userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    userdata = userdata.fetchall()
    ltrord = userdata[0][1]
    multiplier = userdata[0][2]
    
    k = 0
    # I would like to do this without a 'for' loop.
    qh_entries = []
    for k in range(len(hooklist)):
        sql_search_qh = 'SELECT * FROM quiz_hook_' + lex1+'_'+lex2 + \
                        ' WHERE word = ? AND user = ?'
        curr_entry = c.execute(sql_search_qh, (hooklist[k], userid))
        curr_entry = curr_entry.fetchall()
        qh_entries.append(curr_entry[0])
    
    k = 0
    prb_list = []
    for k in range(len(qh_entries)):
        prb_list.append(qh_entries[k][10])
    
    # Now we will begin the quizzing
    quiz = True
    qatt = 0
    qcor = 0
    while quiz:
        # numpy was hard to install on linux, so I didn't use it
        prb_cumsum = my_cumsum(prb_list)
        pick = r.random()*prb_cumsum[-1]
        k = 0
        while pick > prb_cumsum[k]:
            k += 1
        question = qh_entries[k][1]
        fhook1 = qh_entries[k][2]
        fhook2 = qh_entries[k][3]
        bhook1 = qh_entries[k][4]
        bhook2 = qh_entries[k][5]
        fhook_key1 = list(set(fhook1) - set(fhook2))
        fhook_key2 = list(set(fhook2) - set(fhook1))
        fhook_key3 = list(set(fhook1) & set(fhook2))
        bhook_key1 = list(set(bhook1) - set(bhook2))
        bhook_key2 = list(set(bhook2) - set(bhook1))
        bhook_key3 = list(set(bhook1) & set(bhook2))
        fhook_key1 = resort(''.join(fhook_key1), ltrord)
        fhook_key2 = resort(''.join(fhook_key2), ltrord)
        fhook_key3 = resort(''.join(fhook_key3), ltrord)
        bhook_key1 = resort(''.join(bhook_key1), ltrord)
        bhook_key2 = resort(''.join(bhook_key2), ltrord)
        bhook_key3 = resort(''.join(bhook_key3), ltrord)
        if lex_subset:
            fhook_key2 = ''
            bhook_key2 = ''
        endq = False
        print(question)
        print('Front Hooks?')
        fhook_ans1 = input(lex1 +' only? ')
        fhook_ans1 = fhook_ans1.upper()
        fhook_ans1 = resort(fhook_ans1, ltrord)
        fhook_ans2 = ''
        if not lex_subset:
            fhook_ans2 = input(lex2 + ' only? ')
            fhook_ans2 = fhook_ans2.upper()
            fhook_ans2 = resort(fhook_ans2, ltrord)
        fhook_ans3 = input('both ' + lex1 + ' and ' + lex2 + '? ')
        fhook_ans3 = fhook_ans3.upper()
        fhook_ans3 = resort(fhook_ans3, ltrord)
        print('Back Hooks? ')
        bhook_ans1 = input(lex1 +' only? ')
        bhook_ans1 = bhook_ans1.upper()
        bhook_ans1 = resort(bhook_ans1, ltrord)
        bhook_ans2 = ''
        if not lex_subset:
            bhook_ans2 = input(lex2 + ' only? ')
            bhook_ans2 = bhook_ans2.upper()
            bhook_ans2 = resort(bhook_ans2, ltrord)
        bhook_ans3 = input('both ' + lex1 + ' and ' + lex2 + '? ')
        bhook_ans3 = bhook_ans3.upper()
        bhook_ans3 = resort(bhook_ans3, ltrord)
        if fhook_ans3 == 'Q' and bhook_ans3 == 'Q':
            quiz = False
        print('Front Hooks:')
        print(fhook_key1)
        if not lex_subset:
            print(fhook_key2)
        print(fhook_key3)
        print('Back Hooks:')
        print(bhook_key1)
        if not lex_subset:
            print(bhook_key2)
        print(bhook_key3)
        
        answers = []
        for ltr in fhook_key2.join([fhook_key1, fhook_key3]):
            answers.append(ltr + question)
        for ltr in bhook_key2.join([bhook_key1, bhook_key3]):
            answers.append(question + ltr)
        
        answer_data = []
        for word in answers:
            sql = 'SELECT fhook, remfirst, word, remlast, bhook FROM lexicon_' + \
                  lex1 + ' WHERE word = ?'
            word_props = c.execute(sql, (word,))
            word_props = word_props.fetchall()
            answer_data.append(word_props)
        for datum in answer_data:
            print(datum)
        if quiz:
            qatt += 1
            if fhook_ans1 == fhook_key1 and fhook_ans2 == fhook_key2 and \
               fhook_ans3 == fhook_key3 and bhook_ans1 == bhook_key1 and \
               bhook_ans2 == bhook_key2 and bhook_ans3 == bhook_key3:
                qcor += 1
                new_cor = qh_entries[k][6] + 1
                new_inc = qh_entries[k][7]
                natt = new_cor + new_inc
                # This next line could be changed
                # To allow for a user specific number
                # Controls the weighting of more recent responses
                new_wt_cor = qh_entries[k][8] + multiplier
                new_wt_cor *= natt/(natt+multiplier - 1)
                new_wt_inc = qh_entries[k][9]*natt/(natt+multiplier - 1)
                if new_wt_inc >= new_wt_cor:
                    new_prob = 1+new_wt_inc-new_wt_cor
                else:
                    new_prob = 1/(1+new_wt_cor-new_wt_inc)
                qh_entries[k] = (qh_entries[k][0], qh_entries[k][1],\
                                 qh_entries[k][2], qh_entries[k][3],\
                                 qh_entries[k][4], qh_entries[k][5],\
                                 new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob) 
            else:
                new_cor = qh_entries[k][6]
                new_inc = qh_entries[k][7] + 1
                natt = new_cor + new_inc
                # This next line could be changed
                # To allow for a user specific number
                new_wt_inc = qh_entries[k][9] + multiplier
                new_wt_inc *= natt/(natt+multiplier-1)
                new_wt_cor = qh_entries[k][8]*natt/(natt+multiplier-1)
                if new_wt_inc >= new_wt_cor:
                    new_prob = 1+new_wt_inc-new_wt_cor
                else:
                    new_prob = 1/(1+new_wt_cor-new_wt_inc)
                qh_entries[k] = (qh_entries[k][0], qh_entries[k][1],\
                                 qh_entries[k][2], qh_entries[k][3],\
                                 qh_entries[k][4], qh_entries[k][5],\
                                 new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob)
            print(str(new_cor) + '/' + str(new_cor+new_inc) + ' ' +\
                  str(round(new_prob,2)))
            # Updating the database
            sql = 'UPDATE quiz_hook_' + lex1+'_'+lex2 +\
                  ''' SET num_cor = ?,
                          num_inc = ?,
                          wt_cor = ?,
                          wt_inc = ?,
                          prob_val = ?
                      WHERE word = ?'''
            c.execute(sql, (qh_entries[k][6],\
                            qh_entries[k][7],\
                            qh_entries[k][8],\
                            qh_entries[k][9],\
                            qh_entries[k][10],\
                            qh_entries[k][1]))
            conn.commit()
            # Updating probabilities
            prb_list[k] = qh_entries[k][10]
    
    # Displaying statistics
    print('Questions Correct:   ' + str(qcor) + '\n')
    print('Questions Attempted: ' + str(qatt) + '\n')
    print('Thanks for quizzing!')

