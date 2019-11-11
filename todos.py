import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
from termcolor import colored
from tabulate import tabulate

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


def show_list(thingy : None):

    # thingy = input("What do you want to see ? ( users / username / id / complete /  ) ")
    global name
    if type(thingy) is int :  

        sql = """
        SELECT * FROM todos 
        WHERE id = ? 
        """
        cur.execute(sql,(thingy,))
        results = cur.fetchall()
        print(tabulate(results))

    elif thingy == 'users' or thingy == '':
        sql = """
            SELECT * FROM users
            """
        cur.execute(sql)
        results = cur.fetchall()
        print(tabulate(results))

    
    
    elif thingy == 'complete' :
        sql = """
        SELECT * FROM todos
        INNER JOIN users 
        ON todos.userid = users.id
        WHERE name like ? AND status = 'Completed'
        ORDER BY status DESC
        """
        cur.execute(sql,(name,))
        results = cur.fetchall()
        print(tabulate(results))
    

    elif thingy == 'sort' : 
        sql = """
        SELECT * FROM todos
        ORDER BY due_date DESC        
        """
        cur.execute(sql,)
        results = cur.fetchall()
        print(tabulate(results))
    

    elif thingy == 'project' :
        id = input("What's the ID of the project you want to see ? ")
        sql = '''
        SELECT * FROM todos
        LEFT JOIN projects
        ON todos.userid = projects.userid
        WHERE projects.id = ?
        '''
        cur.execute(sql,(id,))
        results = cur.fetchall()
        print(tabulate(results))


    else :
        s = '''
        SELECT * FROM todos
        INNER JOIN users 
        ON todos.userid = users.id
        where name like ?
        ORDER BY due_date ASC
        '''
        cur.execute(s,(thingy, ))
        results = cur.fetchall()
        current_user_id = results[0][0]

        print(tabulate(results))
    
    

def addProject(body) :

    global name

    s = '''
    select * from users where name like ?
    '''
    cur.execute(s,(name, ))
    results = cur.fetchall()
    current_user_id = results[0][0]


    print(colored('Adding Project :','green'), body)
    sql = """
    INSERT INTO projects (name, userid) VALUES (?,?)
    """
    cur.execute(sql,(body, current_user_id))
    conn.commit()

    q = '''
    select * from projects 
    WHERE userid = ? 
    '''
    cur.execute(q,(current_user_id, ))
    results1 = cur.fetchall()
    print(tabulate(results1))
    current_project = results1[0][0]



def whotofire() :
    sql = """
    SELECT users.id, name, email FROM users
    LEFT JOIN todos 
    ON todos.userid = users.id
    WHERE body IS NULL 
    """
    cur.execute(sql,)
    results = cur.fetchall()
    print(tabulate(results))


def show_help_menu() :
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('Todo List Options :','green'))
    print(colored('*' * 50, 'green'))
    print(colored('1. List all todos:', 'green'))
    print(colored('\t python3 todos.py list command', 'white'))
    print(colored('\t command : users / name / sort / complete / project / ', 'white'))
    print(colored('2. Add a new todo:', 'green'))
    print(colored('\t python3 todos.py add', 'white'))
    print(colored('3. Modify a new todo:', 'green'))
    print(colored('\t python3 todos.py add', 'white'))
    print(colored('4. Add a new project:', 'green'))
    print(colored('\t python3 todos.py add_project project_name', 'white'))
    print(colored('4. Delete a todo:', 'green'))
    print(colored('\t python3 todos.py delete', 'white'))
    print(colored('5. Mark a todo complete:', 'green'))
    print(colored('\t python3 todos.py do', 'white'))
    print(colored('6. Mark a todo uncomplete:', 'green'))
    print(colored('\t python3 todos.py undo', 'white'))
    print(colored('7. View the people who fire:', 'green'))
    print(colored('\t python3 todos.py who_to_fire', 'white'))
    print(colored('8. Sign Up ★★★★★ (You must sign up first):', 'red'))
    print(colored('\t python3 todos.py signup', 'white'))
    print(colored('-' * 100, 'green'))


def signup() :
    global name
    email = input("What's your Email? ")
    sql = 'insert into users (name, email) values (?, ?)'
    cur.execute(sql, (name,email))
    conn.commit()


if __name__  == '__main__':
    # try :
        name = input("What's your name? ")
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
                'signup' : signup,
                'add_project' : addProject,
                'whotofire' : whotofire
            })

    # except IndexError:
    #     show_help_menu()
    #     sys.exit(1)






