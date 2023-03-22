import psycopg2

class Db():
    def __init__(selfo, hostname, database, username, port, password):

        self.hostname = hostname
        self.database = database
        self.username = username
        self.port     = port
        self.password = password

        self.get_db_connection()
        self.create_table()

    def get_db_connection(self):
        conn = psycopg2.connect(
                host   = self.hostname,
                dbname = self.database,
                user   = self.username,
                port   = self.port,
                password = self.password)
        cur = conn.cursor()
        return conn, cur

    def create_table(self):
        conn, cur = self.get_db_connection()
        command = """create table if not exists users(
                        id serial primary key,
                        username varchar(40) not null,
                        email varchar(40) unique not null,
                        password varchar(40) not null
                        )"""  
        cur.execute(command)
        conn.commit()

        cur.close()
        conn.close()

    def insert(self, values):
        conn, cur = self.get_db_connection()
        command = '''
            insert into users(username, email, password)
            values(%s,%s,%s)
            '''.format(values)

        cur.execute(command, values)
        conn.commit()

        cur.close()
        conn.close()

    def get(self, column1, column2, value):
        conn, cur = self.get_db_connection()
        command = f'''
            select {column1} from users where {column2}=%s
            '''.format(column1, column2)
        
        cur.execute(command, (value,))
        data = cur.fetchone()
        if data:
            cur.close()
            conn.close()
            return data[0] 

