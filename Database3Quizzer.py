import sqlite3
import random as r

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
    # Adapted from the sqlite tutorial used in '02TableCreation.py'
    
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

# This can be changed, if I want a new format.
createtable = False

database = "Scrabble_Database.db"
conn = sqlite3.connect(database)

# Table for anagram quizzes
if createtable:
    drop_table(conn, 'DROP TABLE IF EXISTS quiz_anag')
    
    sql_create = """ CREATE TABLE IF NOT EXISTS quiz_anag(
                         user text NOT NULL,
                         gram text NOT NULL,
                         answers_twl text,
                         num_cor integer,
                         num_inc integer,
                         wt_cor double,
                         wt_inc double,
                         prob_val double,
                         FOREIGN KEY (user) REFERENCES users (user)
                     ); """
    create_table(conn, sql_create)

# Table for hook quizzes
if createtable:
    drop_table(conn, 'DROP TABLE IF EXISTS quiz_hook')
    
    sql_create = """ CREATE TABLE IF NOT EXISTS quiz_hook(
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
                     ); """
    create_table(conn, sql_create)


# To create users, if desired
def create_user(conn, username, ltrorder):
    """
    Creating a new user
    """
    sql = ''' INSERT INTO users(user, letterorder)
              VALUES(?,?) '''
    cur = conn.cursor()
    userrow = (username, ltrorder)
    cur.execute(sql, userrow)
    return(cur.lastrowid)

def extract_list(lname):
    c = conn.cursor()
    outlist = c.execute('SELECT * FROM gram_table WHERE listname = ?', (lname,))
    outlist = outlist.fetchall()
    output = []
    for k in range(len(outlist)):
        output.append(outlist[k][1])
    return(output)


# Creating a function for anagram quizzes
# You can either use a list, saved as a python list
# ... or a names of a word list from `gram_table`
def quiz_anag(gramlist, userid, listname = True):
    
    # It could be good to do multiple lists at the same time.
    if listname:
        gramlist = extract_list(gramlist)
    c = conn.cursor()
    
    print('You are quizzing!')   
    
    # Using the user specified letter order
    ltrord = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    ltrord = ltrord.fetchall()
    ltrord = ltrord[0][1]
    
    k = 0
    # I would like to do this without a 'for' loop.
    qa_entries = []
    for k in range(len(gramlist)):
        sql_search_qa = 'SELECT * FROM quiz_anag WHERE gram = ? AND user = ?'
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
            sql_search_lex = 'SELECT * FROM lexicon_twl WHERE gram = ?'
            curr_entry = c.execute(sql_search_lex, (gramlist[k],))
            lex_entries.extend(curr_entry.fetchall())
            #if len(lex_entries) > 0:
                #print(len(lex_entries), lex_entries[-1])
        
        gramprev = ''
        answers = ''
        for k in range(len(lex_entries)):
            gram = lex_entries[k][0]
            #print(str(len(answers.split('_'))), gram, gramprev, sep = ' ')
            if k > 0 and gram != gramprev:
                if answers == '':
                    print(k)
                    print(gramprev)
                    break
                sql = '''INSERT INTO quiz_anag(user,gram,answers_twl,num_cor,num_inc,wt_cor,wt_inc,prob_val)
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
        
        sql = '''INSERT INTO quiz_anag(user,gram,answers_twl,num_cor,num_inc,wt_cor,wt_inc,prob_val)
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
            sql = '''INSERT INTO quiz_anag(user,gram,answers_twl,num_cor,num_inc,wt_cor,wt_inc,prob_val)
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
                     FROM lexicon_twl WHERE word = ?'''
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
            new_wt_cor = qa_entries[k][5] + 1.3
            new_wt_cor *= natt/(natt+.3)
            new_wt_inc = qa_entries[k][6]*natt/(natt+.3)
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
            new_wt_inc = qa_entries[k][6] + 1.3
            new_wt_inc *= natt/(natt+.3)
            new_wt_cor = qa_entries[k][5]*natt/(natt+.3)
            if new_wt_inc >= new_wt_cor:
                new_prob = 1+new_wt_inc-new_wt_cor
            else:
                new_prob = 1/(1+new_wt_cor-new_wt_inc)
            qa_entries[k] = (qa_entries[k][0], qa_entries[k][1], qa_entries[k][2],\
                             new_cor, new_inc, new_wt_cor, new_wt_inc, new_prob)
        print(str(new_cor) + '/' + str(new_cor+new_inc) + ' ' +\
              str(round(new_prob,2)))
        # Updating the database
        sql = '''UPDATE quiz_anag
                 SET num_cor = ?,
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
def extract_hook(lname):
    c = conn.cursor()
    outlist = c.execute('SELECT * FROM hook_table WHERE listname = ?', (lname,))
    outlist = outlist.fetchall()
    output = []
    for k in range(len(outlist)):
        output.append(outlist[k][1])
    return(output)

def quiz_hook(list_len, userid, listname = True):
    hooklist = []
    c = conn.cursor()
    # It could be good to do multiple lists at the same time.
    if str(type(list_len)) == "<class 'int'>":
        hookcheck = 'SELECT * FROM lexicon_twl WHERE length = ?'
        datalist = c.execute(hookcheck, (list_len,))
        datalist = datalist.fetchall()
        for data in datalist:
            hooklist.append(data[1])
    
    if str(type(list_len)) == "<class 'str'>":   
        if listname:
            hooklist = extract_hook(list_len)
    
    # Adding entries to quiz_hook if necessary.
    for word in hooklist:
        hookcheck = 'SELECT * FROM quiz_hook WHERE word = ?'
        hookcheck = c.execute(hookcheck, (word,))
        hookcheck = hookcheck.fetchall()
        if len(hookcheck) == 0:
            adddata = 'SELECT * FROM lexicon_twl WHERE word = ?'
            adddata = c.execute(adddata, (word,))
            adddata = adddata.fetchall()
            hookadd = '''INSERT INTO quiz_hook(user, word, fhook, bhook,
                                               num_cor, num_inc, wt_cor, wt_inc,
                                               prob_val)
                         VALUES(?,?,?,?,?,?,?,?,?)'''
            c.execute(hookadd, (userid, word, adddata[0][9], adddata[0][10],\
                                0,0,0,0,5))
            conn.commit()
    
    print('You are quizzing!')   
    
    # Using the user specified letter order
    ltrord = c.execute('SELECT * FROM users WHERE user = ?', (userid,))
    ltrord = ltrord.fetchall()
    ltrord = ltrord[0][1]
    
    k = 0
    # I would like to do this without a 'for' loop.
    qh_entries = []
    for k in range(len(hooklist)):
        sql_search_qh = 'SELECT * FROM quiz_hook WHERE word = ? AND user = ?'
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
            sql = '''SELECT fhook, remfirst, word, remlast, bhook
                     FROM lexicon_twl WHERE word = ?'''
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
                new_wt_cor = qh_entries[k][6] + 1.3
                new_wt_cor *= natt/(natt+.3)
                new_wt_inc = qh_entries[k][7]*natt/(natt+.3)
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
                new_wt_inc = qh_entries[k][7] + 1.3
                new_wt_inc *= natt/(natt+.3)
                new_wt_cor = qh_entries[k][6]*natt/(natt+.3)
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
            sql = '''UPDATE quiz_hook
                     SET num_cor = ?,
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
