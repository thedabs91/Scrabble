import sqlite3
import random as r
import string
from functools import partial

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
    conn.commit()

def quiz_anag_mlex_db(lexlist):
    if len(lexlist) == 1:
        quiz_anag_db(lexlist[0])
    else:
        leges = ''
        for lex in lexlist:
            leges += lex+'_'
        leges = leges.rstrip('_')
        sql_create = 'CREATE TABLE IF NOT EXISTS quiz_anag_' + leges +\
                     '''(   
                            user text NOT NULL,
                            gram text NOT NULL,
                            answers text,
                            lexica text,
                            num_cor integer,
                            num_inc integer,
                            wt_cor double,
                            wt_inc double,
                            prob_val double,
                            FOREIGN KEY (user) REFERENCES users (user)
                        );'''
        create_table(conn, sql_create)
        conn.commit()


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

def quiz_hook_mlex_db(lexlist):
    leges = ''
    for lex in lexlist:
        leges += lex+'_'
    leges = leges.rstrip('_')
    sql_create = 'CREATE TABLE IF NOT EXISTS quiz_hook_' + leges +\
                  '''(
                         user text NOT NULL,
                         word text NOT NULL,
                         lex_id text,
                         fhook text,
                         bhook text,
                         fhook_lex text,
                         bhook_lex text,
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



# Creating a function for anagram quizzes
# You can either use a list, saved as a python list
# ... or a names of a word list from `gram_table`
def quiz_anag(gramlist, userid = None, lexicon = None, listname = True):
    
    # Starting the cursor
    c = conn.cursor()
    
    # Using default lexicon if unspecified
    if lexicon == None or lexicon == 0:
        sql = 'SELECT lexicon FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexicon = usr_lex[0][0]
        print(lexicon)
    
    if lexicon == 1:
        sql = 'SELECT lexicon1 FROM users WHERE user = ?'
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
    initvalue = userdata[0][2]
    multiplier = userdata[0][3]
    
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
                c.execute(sql, (userid, gramprev, answers, 0,0,0,0, initvalue))
                qa_entries.append((userid, gramprev, answers, 0,0,0,0, initvalue))
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
        c.execute(sql, (userid, gramprev, answers, 0,0,0,0, initvalue))
        qa_entries.append((userid, gramprev, answers, 0,0,0,0, initvalue))
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
            c.execute(sql, (userid, gram, '', 0,0,0,0, initvalue))
            qa_entries.append((userid, gram, '', 0,0,0,0, initvalue))
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

def quiz_hook(list_len, userid = None, lexicon = None, listname = True):
    hooklist = []
    c = conn.cursor()
    
    # Using default lexicon if unspecified
    if lexicon == None or lexicon == 0:
        sql = 'SELECT lexicon FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexicon = usr_lex[0][0]
        print(lexicon)
    
    if lexicon == 1:
        sql = 'SELECT lexicon1 FROM users WHERE user = ?'
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
    
    # Using the user specified letter order and multiplier
    userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    userdata = userdata.fetchall()
    ltrord = userdata[0][1]
    initvalue = userdata[0][2]
    multiplier = userdata[0][3]
    
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
                                0,0,0,0, initvalue))
            conn.commit()
    
    print('You are quizzing!')
    
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


#################



## CREATING MULTILEXICAL QUIZZES

# Now I am editing these functions to be multilexical!
def quiz_anag_mlex(gramlist, userid = None, lexlist = None,
                   listname = True):
    # This quiz will be bilexical
    # This makes no assumptions of a lexicon being a subset
    # ... of another lexicon
    
    c = conn.cursor()
    
    
    # Using default lexica if unspecified
    # DOUBLE CHECK AFTER lexlist CREATED IN users DATABASE!!
    if lexlist == None:
        sql = 'SELECT lexlist FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        lexlist = usr_lex[0][0]
        lexlist = lexlist.split('_')
    
    # Stating the lexicon list for additional reference.
    print('lexlist = ')
    k = 0
    for lex in lexlist:
        print(str(k) + ': ' + lex)
        k += 1
    
    # It is useful to create a string of lexica for use
    if len(lexlist) == 1:
        quiz_anag(gramlist, userid = userid, lexicon = lexlist[0],
                  listname = listname)
    else:
        leges = ''
        default_suffix = ''
        for k in range(len(lexlist)):
            leges += lexlist[k]+'_'
            default_suffix += str(k)
        leges = leges.rstrip('_')
        
    
        # It could be good to do multiple lists at the same time.
        gramlistlist = []
        if listname:
            for k in range(len(lexlist)):
                gramlistlist += extract_list(gramlist, lexlist[k])
            # Combining into 1.
            gramlist = list(set(gramlistlist))
            gramlist.sort()
            # To save space for later ...?
            gramlistlist = None
        # Here I note that I did not save the lexica for each answer!
        # These were not answers, they were grams.
                
            
        
        print('You are quizzing!')   
        
        # Using the user specified letter order and multiplier
        userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
        userdata = userdata.fetchall()
        ltrord = userdata[0][1]
        initvalue = userdata[0][2]
        multiplier = userdata[0][3]
        
        k = 0
        # Incorporating elements previously in the quiz_anag table
        qa_entries = []
        for k in range(len(gramlist)):
            sql_search_qa = 'SELECT * FROM quiz_anag_' + leges +\
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
        
        # Now I will search the dictionary for any new information
        if len(gramlist) > 0:
            print(len(gramlist))
            lex_answers = []
            for k in range(len(gramlist)):
                gram_answers = []
                answers_lexica = []
                for ell in range(len(lexlist)):
                    # lexicon lex
                    sql_search_lex = 'SELECT * FROM lexicon_' + lexlist[ell] + ' WHERE gram = ?' 
                    curr_entries = c.execute(sql_search_lex, (gramlist[k],))
                    curr_entries = curr_entries.fetchall()
                    curr_words = []
                    for entry in curr_entries:
                        # Only saving the word for now
                        word = entry[1]
                        curr_words.append(word)
                        if not (word in gram_answers):
                            gram_answers.append(word)
                            answers_lexica.append('')
                    for m in range(len(gram_answers)):
                        if gram_answers[m] in curr_words:
                            answers_lexica[m] += str(ell)
                # Sorting simultaneously
                # Combining into two lists, sorting, then separating back.
                zipsort = zip(gram_answers, answers_lexica)
                zipsort = sorted(zipsort)
                gram_answers, answers_lexica = (list(tuple) for tuple in zip(*zipsort))
                # Converting lists to strings
                gram_ans_str = ''
                ans_lex_str = ''
                for ell in range(len(gram_answers)):
                    if ell > 0:
                        gram_ans_str += '_'
                        ans_lex_str += '_'
                    gram_ans_str += gram_answers[ell]
                    ans_lex_str += answers_lexica[ell]
                # Appending results
                lex_answers.append([gramlist[k], gram_ans_str, ans_lex_str])
            
            
            for k in range(len(lex_answers)):
                sql = 'INSERT INTO quiz_anag_' + leges +\
                      '''(user,gram,answers,lexica,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                         VALUES(?,?,?,?,?,?,?,?,?)'''
                c.execute(sql, (userid, lex_answers[k][0], lex_answers[k][1],\
                                   lex_answers[k][2], 0,0,0,0, initvalue))
                qa_entries.append((userid, lex_answers[k][0], lex_answers[k][1],\
                                   lex_answers[k][2], 0,0,0,0, initvalue))
                prb_list.append(5)
            
                try:
                    gramlist.remove(lex_answers[k][0])
                except ValueError:
                    print(lex_answers[k][0])
                # I don't think I need to worry about gramlist1 and gramlist2.
        conn.commit()
        
        # If anything is left, it has no anagrams
        if len(gramlist) > 0:
            for gram in gramlist:
                sql = 'INSERT INTO quiz_anag_' + leges +\
                      '''(user,gram,answers,lexica,num_cor,num_inc,wt_cor,wt_inc,prob_val)
                         VALUES(?,?,?,?,?,?,?,?,?)'''
                c.execute(sql, (userid, gram, '', '', 0,0,0,0, initvalue))
                qa_entries.append((userid, gram, '', '', 0,0,0,0, initvalue))
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
            anslex = qa_entries[k][3].split('_')
            ans_dic = {}
            for ell in range(len(answers)):
                try:
                    ans_dic[anslex[ell]].append(answers[ell])
                except KeyError:
                    ans_dic[anslex[ell]] = [answers[ell]]
            answers = [answers[ell]+anslex[ell] for ell in range(len(answers))]
            # The question
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
            
            for ell in range(len(replylist)):
                if not replylist[ell][-1].isdigit():
                    replylist[ell] += default_suffix
            
            # Showing the answers
            for key in ans_dic:
                print(key + ': ' + str(ans_dic[key]))
            answer_data = []
            # I do not show data about the answers here
            # ... for now.
            qatt += 1
            if replylist == answers:
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
            sql = 'UPDATE quiz_anag_' + leges +\
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




# Next is a Hook quiz






# A useful function
# Creates a list of letters and the numbers corresponding to the correct lexica
# There is likely a better solution (re library?)
def hooksplit(str):
    str = str.upper()
    out = []
    ctr = -1
    for char in str:
        if char in string.ascii_uppercase:
            ctr += 1
            out.insert(ctr, char)
        else:
            out[ctr] += char
    return(out)




def quiz_hook_mlex(list_len, userid = None, lexlist = None,\
                   listname = True, lex_subset = True):
    hooklist = []
    c = conn.cursor()
    
    # Using default lexica if unspecified
    if lexlist == None:
        sql = 'SELECT lexlist FROM users WHERE user = ?'
        usr_lex = c.execute(sql, (userid,))
        usr_lex = usr_lex.fetchall()
        leges = usr_lex[0][0]
        leges = leges.strip()
        lexlist = leges.split('_')
    else:
        leges = '_'.join(lexlist)
    
    # Ensuring 10 or fewer lexica
    numlex = len(lexlist)
    if numlex > 10:
        print('Too many lexica! Try fewer!')
        lexlist = []
        k = 0
        stop == False
        while stop == False:
            newlex = input('Lexicon ' + k + ': ')
            k += 1
            if newlex == 'q':
                stop = True
            else:
                lexlist.append(newlex)
            if k == 10:
                stop = True
        numlex = len(lexlist)
    
    # Showing lexica to the user
    print('lexica:')
    k = 0
    for lex in lexlist:
        print(str(k) + ': ' + lex)
        k += 1
    
    # It could be good to do multiple lists at the same time.
    # Using all words of the specified length for numerical input
    if str(type(list_len)) == "<class 'int'>":
        datalist = []
        for k in range(numlex):
            hookcheck = 'SELECT * FROM lexicon_' + lexlist[k] + ' WHERE length = ?'
            datalist_k = c.execute(hookcheck, (list_len,))
            datalist_k = datalist_k.fetchall()
            datalist.extend(datalist_k)
        for data in datalist:
            hooklist.append(data[1])
    # Using a named list in the case of string input
    if str(type(list_len)) == "<class 'str'>":   
        if listname:
            hooklist = []
            for k in range(numlex):
                hooklist.extend(extract_hook(list_len, lexlist[k]))
    # Removing duplicates
    hooklist = list(set(hooklist))
    
    # Using the user specified letter order and multiplier
    userdata = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    userdata = userdata.fetchall()
    ltrord = userdata[0][1]
    initvalue = userdata[0][2]
    multiplier = userdata[0][3]
    
    # Adding entries to quiz_hook if necessary.
    # This seems like updating to me
    for word in hooklist:
        lex_id_k = ''
        hookcheck = 'SELECT * FROM quiz_hook_' + leges + ' WHERE word = ?'
        hookcheck = c.execute(hookcheck, (word,))
        hookcheck = hookcheck.fetchall()
        # Adding in hooks if the word was not already in the hook quiz database
        if len(hookcheck) == 0:
            # fhooks and bhooks will be lists of the hooks in each lexicon
            fhooks = []
            bhooks = []
            for k in range(numlex):
                 adddata_k = 'SELECT * FROM lexicon_' + lexlist[k] + ' WHERE word = ?'
                 adddata_k = c.execute(adddata_k, (word,))
                 adddata_k = adddata_k.fetchall()
                 if len(adddata_k) > 0:
                     lex_id_k += str(k)
                     fhooks.append(adddata_k[0][9])
                     bhooks.append(adddata_k[0][10])
                 else:
                     # In this case, the word was not in lexicon k.
                     fhook_k = ''
                     bhook_k = ''
                     for letr in string.ascii_uppercase:
                         # Checking for front hooks
                         adddata_k = 'SELECT * FROM lexicon_' + lexlist[k] +\
                                     ' WHERE word = ?'
                         adddata_k = c.execute(adddata_k, (letr+word,))
                         adddata_k = adddata_k.fetchall()
                         if len(adddata_k) > 0:
                             fhook_k += letr
                         # Checking for back hooks
                         adddata_k = 'SELECT * FROM lexicon_' + lexlist[k] +\
                                     ' WHERE word = ?'
                         adddata_k = c.execute(adddata_k, (word+letr,))
                         adddata_k = adddata_k.fetchall()
                         if len(adddata_k) > 0:
                             bhook_k += letr
                     fhooks.append(fhook_k)
                     bhooks.append(bhook_k)
            # Creating a string of all hooks and a list of the lexica per hook
            # Front Hooks
            pos = 0
            fhook_new = list(set(''.join(fhooks)))
            fhook_new.sort()
            fhook_new = ''.join(fhook_new)
            fhook_lex_new = []
            for hk in fhook_new:
                fhook_lex_new.append('')
                for k in range(numlex):
                    if hk in fhooks[k]:
                        fhook_lex_new[pos] += str(k)
                pos += 1
            # Back Hooks
            pos = 0
            bhook_new = list(set(''.join(bhooks)))
            bhook_new.sort()
            bhook_new = ''.join(bhook_new)
            bhook_lex_new = []
            for hk in bhook_new:
                bhook_lex_new.append('')
                for k in range(numlex):
                    if hk in bhooks[k]:
                        bhook_lex_new[pos] += str(k)
                pos += 1
            # Turn the hook lex list to a string and commit to the database
            fhook_lex_new = '_'.join(fhook_lex_new)
            bhook_lex_new = '_'.join(bhook_lex_new)
            # Adding the entry into the database
            sql = 'INSERT INTO quiz_hook_' + leges +\
                   '''(user,word,lex_id,fhook,bhook,fhook_lex,bhook_lex,
                       num_cor,num_inc,wt_cor,wt_inc,prob_val)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''
            c.execute(sql, (userid, word, lex_id_k, fhook_new, bhook_new,\
                            fhook_lex_new, bhook_lex_new, 0,0,0,0, initvalue))
            conn.commit()
    
    print('You are quizzing!\n')
    
    k = 0
    # I would like to do this without a 'for' loop.
    qh_entries = []
    for k in range(len(hooklist)):
        sql_search_qh = 'SELECT * FROM quiz_hook_' + leges + \
                        ' WHERE word = ? AND user = ?'
        curr_entry = c.execute(sql_search_qh, (hooklist[k], userid))
        curr_entry = curr_entry.fetchall()
        qh_entries.append(curr_entry[0])
    
    k = 0
    prb_list = []
    for k in range(len(qh_entries)):
        prb_list.append(qh_entries[k][11])
    
    # One last constant: the alllex string
    alllex = ''
    for k in range(numlex):
        alllex += str(k)
    
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
        lex_id = qh_entries[k][2]
        fhook = qh_entries[k][3]
        bhook = qh_entries[k][4]
        fhook_lex = qh_entries[k][5]
        bhook_lex = qh_entries[k][6]
        
        endq = False
        print(question)
        lex_id_ans = input('Lexica of above (increasing numbers, no spaces): ')
        lex_id_ans = lex_id_ans.upper()
        fhook_ans = input('Front Hooks?: ')
        fhook_ans = fhook_ans.upper()
        bhook_ans = input('Back Hooks?: ')
        bhook_ans = bhook_ans.upper()
        if lex_id_ans == 'Q':
            quiz = False
        print('')
        
        # Taking and sorting answers
        fhook_alist = hooksplit(fhook_ans)
        fhook_alist.sort()
        fhook_leges = fhook_lex.split('_')
        bhook_alist = hooksplit(bhook_ans)
        bhook_alist.sort()
        bhook_leges = bhook_lex.split('_')
        
        fhook_acheck = ''.join(fhook_alist)
        fhook_acheck = fhook_acheck.replace(alllex, '')
        bhook_acheck = ''.join(bhook_alist)
        bhook_acheck = bhook_acheck.replace(alllex, '')
        # This code could be replaced if I change how to save the answers here
        fhook_corans = ''
        for k in range(len(fhook)):
            fhook_corans += fhook[k]
            if fhook_leges[k] != alllex:
                fhook_corans += fhook_leges[k]
        bhook_corans = ''
        for k in range(len(bhook)):
            bhook_corans += bhook[k]
            if bhook_leges[k] != alllex:
                bhook_corans += bhook_leges[k]
        
        print('Lexica of base word: ' + lex_id)
        print('Front Hooks')
        print('-----------')
        print('You: ' + fhook_acheck)
        print('Key: ' + fhook_corans + '\n')
        print('Back Hooks')
        print('----------')
        print('You: ' + bhook_acheck)
        print('Key: ' + bhook_corans + '\n')
        
        # Checking the user's work
        qatt += 1
        # Checking against the key
        correct = (fhook_acheck == fhook_corans and\
                   bhook_acheck == bhook_corans and\
                   (lex_id_ans == lex_id or not quiz))
        
        
        # Updating the database based on the answer
        if correct:
            qcor += 1
            new_cor = qh_entries[k][7] + 1
            new_inc = qh_entries[k][8]
            natt = new_cor + new_inc
            # This next line could be changed
            # To allow for a user specific number
            # Controls the weighting of more recent responses
            new_wt_cor = qh_entries[k][9] + multiplier
            new_wt_cor *= natt/(natt+multiplier - 1)
            new_wt_inc = qh_entries[k][10]*natt/(natt+multiplier - 1)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qh_entries[k] = (qh_entries[k][0], qh_entries[k][1], qh_entries[k][2],\
                             qh_entries[k][3], qh_entries[k][4],\
                             qh_entries[k][5], qh_entries[k][6],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob) 
        else:
            new_cor = qh_entries[k][7]
            new_inc = qh_entries[k][8] + 1
            natt = new_cor + new_inc
            # This next line could be changed
            # To allow for a user specific number
            new_wt_inc = qh_entries[k][10] + multiplier
            new_wt_inc *= natt/(natt+multiplier-1)
            new_wt_cor = qh_entries[k][9]*natt/(natt+multiplier-1)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qh_entries[k] = (qh_entries[k][0], qh_entries[k][1], qh_entries[k][2],\
                             qh_entries[k][3], qh_entries[k][4],\
                             qh_entries[k][5], qh_entries[k][6],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob)
        
        print(str(new_cor) + '/' + str(new_cor+new_inc) + ' ' +\
              str(round(new_prob,2)))
        # Updating the database
        sql = 'UPDATE quiz_hook_' + leges +\
              ''' SET num_cor = ?,
                      num_inc = ?,
                      wt_cor = ?,
                      wt_inc = ?,
                      prob_val = ?
                  WHERE word = ?'''
        c.execute(sql, (qh_entries[k][7],\
                        qh_entries[k][8],\
                        qh_entries[k][9],\
                        qh_entries[k][10],\
                        qh_entries[k][11],\
                        qh_entries[k][1]))
        conn.commit()
        # Updating probabilities
        prb_list[k] = qh_entries[k][10]
    
    # Displaying statistics
    if not quiz:
        print('Questions Correct:   ' + str(qcor) + '\n')
        print('Questions Attempted: ' + str(qatt) + '\n')
        print('Thanks for quizzing!')











### Creating an opportunity to login:
def login_fxn():
    c = conn.cursor()
    uname_global = None
    login_code = False
    while(login_code == False):
        login = input('Would you like to login (y/n)?: ')
        if login.lower() == 'y':
            uname_global = input('Username: ')
            login_code = True
            # Editing function defaults?
            global quiz_hook
            global quiz_anag
            global quiz_hook_mlex
            global quiz_anag_mlex
            quiz_hook = partial(quiz_hook, userid = uname_global)
            quiz_anag = partial(quiz_anag, userid = uname_global)
            quiz_hook_mlex = partial(quiz_hook_mlex, userid = uname_global)
            quiz_anag_mlex = partial(quiz_anag_mlex, userid = uname_global)
            usrupd_code = input('Would you like to update defaults (y/n)?: ')
            # If you would want to update information on the defaults.
            if usrupd_code.lower() == 'y':
                lex_code = input('Update lexica (y/n)?: ')
                if lex_code.lower() == 'y':
                    print('If you do not want to update a lexicon, type the letter "n".')
                    print('If you do want to update, type the name of the lexicon.')
                    lexicon_new = input('Preferred lexicon for unilexical quizzes: ')
                    lexicon_new = lexicon_new.strip(' ')
                    if lexicon_new.lower() == 'n':
                        sql = 'SELECT lexicon FROM users WHERE user = ?'
                        lex_sql = c.execute(sql, (uname_global,))
                        lex_sql = lex_sql.fetchall()
                        lexicon = lex_sql[0][0]
                    lexicon1_new = input('Preferred secondary lexicon: ')
                    lexicon1_new = lexicon_new.strip(' ')
                    if lexicon1_new.lower() == 'n':
                        sql = 'SELECT lexicon1 FROM users WHERE user = ?'
                        lex_sql = c.execute(sql, (uname_global,))
                        lex_sql = lex_sql.fetchall()
                        lexicon1 = lex_sql[0][0]
                    print('To update multilex lexica, type the new lexica in order separated by commas.')
                    mlex_new = input('Multilex lexica: ')
                    if mlex_new.lower() == 'n':
                        sql = 'SELECT lexlist FROM users WHERE user = ?'
                        lex_sql = c.execute(sql, (uname_global,))
                        lex_sql = lex_sql.fetchall()
                        lexlist_new = lex_sql[0][0]
                    else:
                        mlex_new = mlex_new.split(',')
                        mlex_new = [lex.strip() for lex in mlex_new]
                        lexlist_new = '_'.join(mlex_new)
                    sql = '''UPDATE users SET lexicon = ?, lexicon1 = ?,
                             lexlist = ? WHERE user = ?'''
                    c.execute(sql, (lexicon_new, lexicon1_new, lexlist_new, uname_global))
                    conn.commit()
                ltrord_code = input('Update letter order (y/n)?: ')
                if ltrord_code.lower() == 'y':
                    ltrord_legal = False
                    while not ltrord_legal:
                        ltrord_new = input('New letter order (type "n" to cancel): ')
                        ltrord_new = ltrord_new.upper()
                        if ltrord_new == 'n':
                            sql = 'SELECT letterorder FROM users WHERE user = ?'
                            ltrord_new = c.execute(sql, (uname_global,))
                        ltrord_legal = ltrord_check(ltrord_new)
                        if not ltrord_legal:
                            print('Illegal letter order. Try again.')
                    sql = 'UPDATE users SET letterorder = ? WHERE user = ?'
                    c.execute(sql, (ltrord_new, uname_global))
                    conn.commit()
                init_code = input('Update initial value (y/n)?: ')
                if init_code == 'y':
                    init_new = float(input('New initial value: '))
                    while (init_new < 2):
                        init_check = input('Are you sure about that number (y/n)?: ')
                        if init_check.lower() == 'y':
                            pass
                        elif init_check.lower() == 'n':
                            init_new = float(input('New initial value: '))
                        else:
                            print('Not "y" or "n". Try again.')
                    sql = 'UPDATE users SET initvalue = ? WHERE user = ?'
                    c.execute(sql, (init_new, uname_global))
                    table_names = c.execute('SELECT name FROM sqlite_schema')
                    table_names = table_names.fetchall()
                    table_names = [name[0] for name in table_names]
                    for name in table_names:
                        if name[:5] == 'quiz_':
                            sql = 'UPDATE ' + name + ''' SET prob_val = ?
                                   WHERE num_cor = 0 AND num_inc = 0 AND user = ?'''
                            c.execute(sql, (init_new, uname_global))
                    conn.commit()
                mult_code = input('Update multiplier (y/n)?: ')
                if mult_code.lower() == 'y':
                    mult_new = float(input('New multiplier: '))
                    while (mult_new < 1) or (mult_new > 2):
                        print('You chose a weird multiplier value.')
                        mult_check = input('Are you sure about that number (y/n)?: ')
                        if mult_check.lower() == 'y':
                            pass
                        elif mult_check.lower() == 'n':
                            mult_new = float(input('New multiplier: '))
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
