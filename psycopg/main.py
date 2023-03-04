import psycopg2

def delete_db(co):
    curs.execute("""
    DROP TABLE phones;
    DROP TABLE clients;
    """)
    print("Tables are deleted")
    conn.commit()

# Функция, создающая структуру БД (таблицы)
def create_db(co):
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
def add_client(conn, name, last_name, email, phone=None):
    with conn.cursor() as curs:
        if find_client(conn, email=email):  # Ищем клиента с таким имейлом
            return print("Данный пользователь уже есть")  # Сообщаем пользователю, что клиент с таким имейлом уже есть
        curs.execute("""
        INSERT INTO clients(name, surname, email) VALUES (%s, %s, %s) RETURNING id;    
        """, (name, last_name, email))
        user = curs.fetchone()[0]
        if phone:
            curs.execute("""
            INSERT INTO phones(phone_, client_id) VALUES (%s, %s);
            """, (phone, user))
            conn.commit()
        return "Данные добавлены"


# Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone):
    with conn.cursor() as curs:
        curs.execute("""
            SELECT phone_ from phones
            WHERE phone_ = %s
            """, (phone,))
        if curs.fetchone():
            return "Данный номер уже есть"
        if not curs.fetchone():
            return "Данный клиент не существует"
        curs.execute("""
        INSERT INTO phones(phone_, client_id) VALUES(%s, %s);
        """, (phone, client_id))

        conn.commit()
    return "Номер текущего клиента добавлен"



# Функция, позволяющая изменить данные о клиенте
def change_client(conn, id, name=None, last_name=None, email=None, old_phone=None, phones=None):
    with conn.cursor() as curs:
        curs.execute("""
            SELECT name, surname, email FROM clients
            WHERE id=%s
            """, (id,))
        user = curs.fetchone()
        if not user:
            return "Клиент не существует"
        user = list(user)
        if name:
            user[0] = name
        if last_name:
            user[1] = last_name
        if email:
            user[2] = email
        curs.execute("""
        UPDATE clients
        SET name=%s, surname=%s, email=%s
        WHERE id=%s
        """, (name, last_name, email, id))
        conn.commit()
        return "Данные клиента изменены"


# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    curs.execute("""
    DELETE FROM phones WHERE client_id=%s;
    DELETE FROM clients WHERE id=%s;   
    """, (client_id, client_id))
    conn.commit()
    return "Запись о клиенте удалена"

# Функция, позволяющая удалить телефонный номер клиента
def delete_phone(name, last_name):
    curs.execute('''
    SELECT id FROM clients WHERE name=%s AND surname=%s;
    ''', (name, last_name))
    res = curs.fetchone()[0]
    curs.execute('''
    DELETE FROM phones WHERE id=%s;
    ''', (res,))
    conn.commit()
    return "Номер удалён"

# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
def find_client(conn, name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as curs:
        if name is None:
            name = "Name"
        if last_name is None:
            last_name = "last_name"
        if email is None:
            email = "email"
        if phone is None:
            phone = "+11111111111"
        user = f"""
                SELECT
                    email
                    name
                    surname
                    CASE
                        WHEN ARRAY_AGG(phone_) = '{{Null}}' THEN ARRAY[]::TEXT[]
                        ELSE ARRAY_AGG(phone_)
                    END phones
                FROM clients
                    LEFT JOIN phones ON clients.id=phones.client_id; 
                    GROUP BY email, name, surname 
                    HAVING name LIKE %s AND surname LIKE %s AND email LIKE %s AND phone_ LIKE %s 
                """
        curs.execute("""
        SELECT name, surname, email, phone_ FROM clients
        LEFT JOIN phones p ON clients.id = p.client_id
        WHERE name=%s OR surname=%s OR email=%s OR phone_=%s;""", (name, last_name, email, phone))
        conn.commit()
        return curs.fetchall()


with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="12345678", port="5432") as conn:
    with conn.cursor() as curs:
        delete_db(conn)
        create_db(conn)
        add_client(conn, 'Иван', 'Петров', 'petrov@bk.ru', '+79041222333')
        add_client(conn, 'Мария', 'Сидорова', 'sidorova@bk.ru', '+79084555666')
        add_phone(conn, 2, '+79855002299')
        delete_phone('Мария', 'Сидорова')
        change_client(conn, id=2, name="Мария", last_name="Сидорова", email='sidorova@bk.ru',
                      phones=None, old_phone=None)
        delete_client(conn, '2')
        find_client(conn, phone='+79041222333')

conn.close()
