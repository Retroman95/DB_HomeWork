import psycopg2

# Функция, создающая структуру БД (таблицы)
def create_db(co):
    curs.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)
    curs.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id  SERIAL PRIMARY KEY,
        name VARCHAR(55) NOT NULL,
        surname VARCHAR(55) NOT NULL,
        email VARCHAR(60) NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        phone_ VARCHAR(40) UNIQUE,
        client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE
    );
    """)
    print("Tables are created")
    conn.commit()


# Функция, позволяющая добавить нового клиента
def add_client(conn, first_name, last_name, email, phone=None):
    curs.execute("""
    INSERT INTO clients(name, surname, email) VALUES (%s, %s, %s) RETURNING id;    
    """, (first_name, last_name, email))
    id_ = curs.fetchone()[0]
    if phone:
        curs.execute("""
        INSERT INTO phones(phone_, client_id) VALUES (%s, %s);
        """, (phone, id_))
        conn.commit()
    print('Data was added')


# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone):
    curs.execute("""
    INSERT INTO phones(phone_, client_id) VALUES(%s, %s);
    """, (phone, client_id))
    conn.commit()
    print('Phone for existing customer added')


# Функция, позволяющая изменить данные о клиенте
def change_client(conn, id, first_name=None, last_name=None, email=None, old_phone=None, phones=None):
    if first_name:
        curs.execute('''UPDATE clients SET name=%s  WHERE id=%s;''',
                    (first_name, id))
    elif last_name:
        curs.execute('''UPDATE clients SET surname=%s WHERE id=%s;''',
                    (last_name, id))
    elif email:
        curs.execute('''UPDATE clients SET email=%s WHERE id=%s;''',
                    (email, id))
    elif old_phone:
        curs.execute('''UPDATE phones Set phone_=%s WHERE phone_=%s;''', (phones, old_phone))
    elif old_phone is None:
        old_phone = input('What phone number to replace?:')
        curs.execute('''UPDATE phones Set phone_=%s WHERE phone_=%s;''', (phones, old_phone))
    conn.commit()
    print('Customer data changed')


# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    curs.execute("""
    DELETE FROM phones WHERE client_id=%s;
    DELETE FROM clients WHERE id=%s;   
    """, (client_id, client_id))
    conn.commit()
    print('Client record deleted')


# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    curs.execute("""
    SELECT name, surname, email, phone_ FROM clients
    LEFT JOIN phones p ON clients.id = p.client_id
    WHERE name=%s OR surname=%s OR email=%s OR phone_=%s;""", (first_name, last_name, email, phone))
    conn.commit()
    return curs.fetchall()


with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="12345678", port="5432") as conn:
    with conn.cursor() as curs:
        create_db(conn)
        add_client(conn, 'Иван', 'Петров', 'petrov@bk.ru', '+79041222333')
        add_client(conn, 'Мария', 'Сидорова', 'sidorova@bk.ru', '+79084555666')
        add_phone(conn, 2, '+79855002299')
        change_client(conn, id=2, first_name=None, last_name="Сидорова", email=None,
                      phones=None, old_phone=None)
        delete_client(conn, '2')
        find_client(conn, phone='+79041222333')

conn.close()
