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
        cur.execute("CREATE TABLE IF NOT EXISTS feedback (id SERIAL PRIMARY KEY, feed boolean, msg VARCHAR(150))")
        print("Tabela feedback criada com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.commit()
        cur.close()
        conn.close()

def alterar_tabela_feedback():
    conn = psycopg2.connect(
        host=env("DB_HOST"),
        database=env("DB_NAME"),
        user=env("DB_USER"),
        password=env("DB_PASS"),
        sslmode='require'
    )
    try:
        cur = conn.cursor()
        
        cur.execute("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS msg VARCHAR(150)")
        print("feedback alterada com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.commit()
        cur.close()
        conn.close()


def inserir_feedback(feedback: Feedback):
    print(feedback.get_feed())
    print(feedback.get_msg())
    conn = psycopg2.connect(
        host=env("DB_HOST"),
        database=env("DB_NAME"),
        user=env("DB_USER"),
        password=env("DB_PASS"),
        sslmode='require'
    )
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS feedback (id SERIAL PRIMARY KEY, feed boolean, msg VARCHAR(150))")
        cur.execute("INSERT INTO feedback (feed, msg) VALUES (%s, %s)", (feedback.get_feed(), feedback.get_msg(),))
        print("Feedback inserido com sucesso!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.commit()
        cur.close()
        conn.close() 