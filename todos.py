import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
from termcolor import colored

name = ''
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()


def do():
    id = int(input('Input the Id : '))
    print(colored('Changing Stutus :','green'), id)
    sql = """
    UPDATE todos 
    SET status = "Completed"
    WHERE id = ?
    """
    cur.execute(sql,(id,))
    conn.commit()




def add():
    body = input('Input the body : ')
    global name
    s = '''
    select * from users where name like ?
    '''
    cur.execute(s,(name, ))
    results = cur.fetchall()
    current_user_id = results[0][0]


    print(colored('Adding Todo :','green'), body)
    sql = """
    INSERT INTO todos (body, due_date, userid) VALUES (?, ?, ?)
    """
    cur.execute(sql,(body, datetime.now(), current_user_id))
    conn.commit()

def modify():
    id = int(input('Input the Id : '))
    print(colored('Modifying Todo :','green'), id)
    print(colored('Input Body contents :','green'))
    content = input()

    sql = """
    UPDATE todos 
    SET body = ?
    WHERE id = ?
    """
    cur.execute(sql,(content,id))
    conn.commit()


def undo():
    id = int(input('Input the Id : '))

    print(colored('Changing Stutus :','green'), id)
    sql = """
    UPDATE todos 
    SET status = "Incompleted"
    WHERE id = ?
    """
    cur.execute(sql,(id,))
    conn.commit()
    


def delete():
    id = int(input('Input the Id : '))
    print(colored('Deleting Todo :','green'),id)
    sql="""
    DELETE FROM todos
    WHERE id = ?
    """
    print('delete')

    cur.execute(sql,(id,))
    conn.commit()


def show_list():

    thingy = input("What do you want to see ? ( all / name / complete )")
    if thingy == 'all' or thingy == None :
        sql = """
            SELECT * FROM todos
            INNER JOIN users 
            ON todos.userid = users.id
            ORDER BY userid DESC
            """
        cur.execute(sql)
        results = cur.fetchall()
        print(results)

    global name

    if thingy == name :
        
        s = '''
        SELECT * FROM todos
        INNER JOIN users 
        ON todos.userid = users.id
        where name like ?
        '''
        cur.execute(s,(name, ))
        results = cur.fetchall()
        current_user_id = results[0][0]

        if results == None :
            print("You can't access")
        else :
            print(results)

        


    
    if thingy == 'complete' :
        sql = """
        SELECT * FROM todos
        INNER JOIN users 
        ON todos.userid = users.id
        WHERE name like ? AND status = 'Completed'
        ORDER BY status DESC
        """
        cur.execute(sql,(name,))
        results = cur.fetchall()
        print(results)
    
    
    
def show_help_menu() :
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('Todo List Options :','green'))
    print(colored('*' * 50, 'green'))
    print(colored('1. List all todos:', 'green'))
    print(colored('\t python3 todos.py list', 'white'))
    print(colored('2. Add a new todo:', 'green'))
    print(colored('\t python3 todos.py add', 'white'))
    print(colored('3. Modify a new todo:', 'green'))
    print(colored('\t python3 todos.py add', 'white'))
    print(colored('4. Delete a todo:', 'green'))
    print(colored('\t python3 todos.py delete', 'white'))
    print(colored('5. Mark a todo complete:', 'green'))
    print(colored('\t python3 todos.py do', 'white'))
    print(colored('6. Mark a todo uncomplete:', 'green'))
    print(colored('\t python3 todos.py undo', 'white'))
    print(colored('7. Sign Up ★★★★★ (You must sign up first):', 'red'))
    print(colored('\t python3 todos.py signup', 'white'))
    print(colored('-' * 100, 'green'))


def signup() :
    global name
    sql = 'insert into users (name) values (?)'
    cur.execute(sql, (name,))
    conn.commit()


if __name__  == '__main__':
    name = input("What 's your name?")
    try :
        arg1 = sys.argv[1]  #we access the flag we pass after python3 todos.py
        if arg1 == '--help':
            show_help_menu()
        else :
            fire.Fire({
                'do' : do,
                'add' : add,
                'undo' : undo,
                'delete' : delete,
                'list' : show_list,
                'modify' : modify,
                'signup' : signup
            })

    except IndexError:
        show_help_menu()
        sys.exit(1)






