import sqlite3
import string

# Writing necessary functions

def connector(db_file):
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

def create_table(create_table_sql):
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


# Creating the 'users' table
database = "Scrabble_Database.db"

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                 user text PRIMARY KEY,
                                 letterorder text NOT NULL,
                                 initvalue integer NOT NULL,
                                 multiplier real NOT NULL,
                                 lexicon text,
                                 lexicon1 text,
                                 lexlist text
                             ); """

conn = connector(database)
if conn is not None:
    create_table(sql_create_users_table)
else:
    print('Error! Cannot create database connection.')


def create_user(username, ltrorder = string.ascii_uppercase,\
                initvalue = 8, multiplier = 1.2,\
                lexicon = None, lexicon1 = None, lexlist = None):
    """
    Creating a new user
    """
    
    checkltrorder = True
    while checkltrorder:
        ltrorder = ltrorder.upper()
        ltrorder_check = [ltr for ltr in ltrorder]
        ltrorder_check.sort()
        ltrorder_check = ''.join(ltrorder_check)
        if ltrorder_check != string.ascii_uppercase:
            print('Letter order invalid, please retry or type "D" for default')
            ltrorder = input(': ')
            if ltrorder.upper() == 'D':
                ltrorder = string.ascii_uppercase()
                checkltrorder = False
        else:
            checkltrorder = False
    
    if lexlist != None:
        lexlist = '_'.join(lexlist)
    
    sql = ''' INSERT INTO users(user, letterorder, multiplier, initvalue,
                                lexicon, lexicon1, lexlist)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    userrow = (username, ltrorder, multiplier, initvalue,\
               lexicon, lexicon1, lexlist)
    cur.execute(sql, userrow)
    conn.commit()
    return(cur.lastrowid)

