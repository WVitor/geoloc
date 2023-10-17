import psycopg2
from os import getenv as env

from model.feedback import Feedback

def criar_tabela_feedback():
    conn = psycopg2.connect(
        host=env("DB_HOST"),
        database=env("DB_NAME"),
        user=env("DB_USER"),
        password=env("DB_PASS"),
        sslmode='require'
    )
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS feedback (id SERIAL PRIMARY KEY, feed boolean)")
        print("Tabela feedback criada com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.commit()
        cur.close()
        conn.close()

def inserir_feedback(feedback: Feedback):
    conn = psycopg2.connect(
        host=env("DB_HOST"),
        database=env("DB_NAME"),
        user=env("DB_USER"),
        password=env("DB_PASS"),
        sslmode='require'
    )
    try:
        cur = conn.cursor()
        if(feedback.get_feed() == True):   
            cur.execute("INSERT INTO feedback (feed) VALUES (true)")
        else:
            cur.execute("INSERT INTO feedback (feed) VALUES (false)")
        print("Feedback inserido com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.commit()
        cur.close()
        conn.close() 