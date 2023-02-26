import psycopg2

def create_db(conn):

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_data
        (id SERIAL PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(40) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_phone(
        id_phone SERIAL PRIMARY KEY,
        client_id INTEGER NOT NULL REFERENCES clients_data(id),
        phone VARCHAR(20) UNIQUE
        );
    """)
    return 

def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute("""
    INSERT INTO clients_data(first_name, last_name, email) VALUES(%s, %s, %s);
    """, (first_name, last_name, email))


def add_phone(conn, client_id, phone):
    cur.execute("""
    INSERT INTO clients_phone(client_id, phone) VALUES(%s, %s);
    """, (client_id, phone))


def change_client(conn, client_id=None, first_name=None, last_name=None, email=None, phones=None):
    print("Для изменения информации о клиенте Вам доступны следующие команды:\n"
    "1 - изменить имя;\n2 - изменить фамилию;\n3 - изменить e-mail;\n4 - изменить номер телефона")

    while True:
        command = int(input('Введите команду: '))
        if command == 1:
            client_id = input("Введите id клиента имя которого хотите изменить: ")
            change_name = input("Введите имя для изменения: ")
            cur.execute("""
            UPDATE clients_data SET first_name=%s WHERE id=%s;
            """, (change_name, client_id))
            break
        elif command == 2:
            client_id = input("Введите id клиента фамилию которого хотите изменить: ")
            change_name = input("Введите фамилию для изменения: ")
            cur.execute("""
            UPDATE clients_data SET last_name=%s WHERE id=%s;
            """, (change_name, client_id))
            break
        elif command == 3:
            client_id = input("Введите id клиента e-mail которого хотите изменить: ")
            change_email = input("Введите e-mail для изменения: ")
            cur.execute("""
            UPDATE clients_data SET email=%s WHERE id=%s;
            """, (change_phone, client_id))
            break
        elif command == 4:
            phone = input("Введите номер телефона который Вы хотите изменить: ")
            change_phone = input("Введите новый номер телефона, который заменит собой старый: ")
            cur.execute("""
            UPDATE clients_phone SET phone=%s WHERE phone=%s;
            """, (change_phone, phone))
            break
        else:
            print("К сожалению, Вы ввели неправильную команду, пожалуйста, повторите ввод")


def delete_phone(conn, client_id=None, phone=None):
    client_id = input("Введите id клиента номер телефона которого хотите удалить: ")
    phone = input("Введите номер телефона который хотите удалить: ")
    cur.execute("""
    DELETE FROM clients_phone WHERE client_id=%s AND phone=%s;
    """, (client_id, phone))


def delete_client(conn, client_id=None):
    client_id = input("Введите id клиента которого хотите удалить: ")
    last_name = input("Введите фамилию клиента которого хотите удалить: ")
    cur.execute("""
    DELETE FROM clients_phone WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    DELETE FROM clients_data WHERE id=%s AND last_name=%s;
    """, (client_id, last_name))


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n"
          "1 - найти по имени;\n2 - найти по фамилии;\n3 - найти по e-mail;\n4 - найти по номеру телефона")
    while True:
        command_finding = int(input("Введите команду для поиска информации о клиенте: "))
        if command_finding == 1:
            first_name_finding = input("Введите имя для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients_data cd
            JOIN clients_phone cp ON cp.client_id = cd.id
            WHERE first_name=%s;
            """, (first_name_finding,))
            print(cur.fetchall())
        elif command_finding == 2:
            last_name_finding = input("Введите фамилию для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients_data cd
            JOIN clients_phone cp ON cp.client_id = cd.id
            WHERE last_name=%s;
            """, (last_name_finding,))
            print(cur.fetchall())
        elif command_finding == 3:
            email_finding = input("Введите email для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients_data cd
            JOIN clients_phone cp ON cp.client_id = cd.id
            WHERE email=%s;
            """, (email_finding,))
            print(cur.fetchall())
        elif command_finding == 4:
            phone_finding = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, last_name, email, phone FROM clients_data cd
            JOIN clients_phone cp ON cp.client_id = cd.id
            WHERE phone=%s;
            """, (phone_finding,))
            print(cur.fetchall())
        else:
            print("К сожалению, Вы ввели неправильную команду, пожалуйста, повторите ввод")


with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="12345678", port="5432") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, "Иван", "Петров", "petrov@bk.ru")
        add_client(cur, "Мария", "Сидорова", "sidorova@bk.ru")
        add_client(cur, "Светлана", "Соколова", "sokolova@bk.ru")
        add_client(cur, "Дмитрий", "Иванов", "ivanov@bk.ru")
        add_client (cur, "Сергей", "Носов", "nosov@bk.ru")
        add_phone(cur, 1, "9041222333")
        add_phone(cur, 2, "9084555666")
        add_phone(cur, 3, "9069555777")
        add_phone(cur, 4, "9648444666")
        add_phone(cur, 3, "9126888222")
        change_client(cur)
        delete_phone(cur)
        delete_client(cur)
        find_client(cur)

conn.commit()

conn.close()
