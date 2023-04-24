import psycopg2


def createDB():
    with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
        with conn.cursor() as cur:
            cur.execute(
                'CREATE TABLE IF NOT EXISTS clients(id SERIAL PRIMARY KEY, name VARCHAR(60), surname VARCHAR(60), '
                'email VARCHAR (60) UNIQUE);')

            cur.execute(
                'CREATE TABLE IF NOT EXISTS phones(client_id INTEGER REFERENCES clients(id), phone VARCHAR(40) UNIQUE, '
                'CONSTRAINT phone_client primary key (client_id, phone));')


def insert_client(name, surname, email, phone=None):
    with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO clients (name, surname , email) VALUES(%s, %s, %s) RETURNING id;',
                        (name, surname, email))
            client_id = cur.fetchone()
            if phone != None:
                cur.execute('INSERT INTO phones (client_id, phone) VALUES(%s, %s);',
                            (client_id, phone))


def insert_phone(client_id, phone):
    with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO phones (client_id, phone) VALUES(%s, %s);',
                        (client_id, phone))

def change_client_info(client_id, name=None, surname=None, email=None, phone=None):
    if name != None:
        with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE clients SET name=%s WHERE id=%s;', (name, client_id))
    if surname != None:
        with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE clients SET surname=%s WHERE id=%s;', (surname, client_id))
    if email != None:
        with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE clients SET email=%s WHERE id=%s;', (email, client_id))
    if phone != None:
        with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
            with conn.cursor() as cur:
                cur.execute('UPDATE phones SET phone=%s WHERE client_id=%s and phone=%s;', (phone, client_id))


def delete_phone(client_id, phone):
    with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM phones WHERE client_id=%s AND phone=%s;', (client_id, phone))


def delete_client(client_id):
    with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM clients WHERE id=%s;', (client_id))


def find_client(name=None, surname=None, email=None, phone=None):
    if phone != None:
        with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
            with conn.cursor() as cur:
                client_id = cur.execute('SELECT client_id FROM phones WHERE phone=%s;', (phone,))
                client_id = cur.fetchone()
                client_id = client_id[0]
                cur.execute('SELECT * FROM clients WHERE id=%s;', (client_id,))
                print(cur.fetchall())
    elif name != None and surname != None and email != None:
        with psycopg2.connect(database="Python", user="postgres", password="6996") as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM clients WHERE name=%s and surname=%s and email=%s;', (name, surname, email))
                print(cur.fetchall())
    else:
        print('Введены некорректные данные')



createDB()

insert_client('Тест', 'Тестов', 'Тест@тест.тест')
insert_client('Иван', 'Иванов', 'Иван@иван.иван', '8-801-555-35-35')

insert_phone(1, '8-800-555-35-35')

change_client_info(1)

delete_phone(3, '8-801-555-35-35')

delete_client('3')

find_client('Тест','Тестов','Тест@тест.тест','8-800-555-35-35')