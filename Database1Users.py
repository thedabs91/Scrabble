import sqlite3

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
                                 multiplier integer NOT NULL,
                                 lexicon text,
                                 lex1 text,
                                 lex2 text,
                                 lixlist text
                             ); """

conn = connector(database)
if conn is not None:
    create_table(sql_create_users_table)
else:
    print('Error! Cannot create database connection.')


def create_user(username, ltrorder, multiplier, lexicon = None,\
                lex1 = None , lex2 = None, lexlist = None):
    """
    Creating a new user
    """
    sql = ''' INSERT INTO users(user, letterorder, multiplier,\
                                lexicon, lex1, lex2, lexlist)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    userrow = (username, ltrorder, multiplier, lexicon, lex1, lex2, lexlist)
    cur.execute(sql, userrow)
    conn.commit()
    return(cur.lastrowid)

