import psycopg2

class Db():
    # Constructor function that initializes the database connection parameters and creates a table if it does not already exist
    def __init__(selfo, hostname, database, username, port, password):
        # Set the database connection parameters
        self.hostname = hostname
        self.database = database
        self.username = username
        self.port     = port
        self.password = password

        # Get a database connection and create the users table
        self.get_db_connection()
        self.create_table()

    # Function that gets a database connection
    def get_db_connection(self):
        # Connect to the database with the specified parameters
        conn = psycopg2.connect(
                host   = self.hostname,
                dbname = self.database,
                user   = self.username,
                port   = self.port,
                password = self.password)
        cur = conn.cursor()
        # Return the connection and cursor objects
        return conn, cur

    # Function that creates a users table if it does not already exist
    def create_table(self):
        # Get a database connection and create the users table if it does not exist
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

    # Function that inserts a new user into the users table
    def insert(self, values):
        # Get a database connection and insert the values into the users table
        conn, cur = self.get_db_connection()
        command = '''
            insert into users(username, email, password)
            values(%s,%s,%s)
            '''.format(values)

        cur.execute(command, values)
        conn.commit()

        cur.close()
        conn.close()

    # Function that gets a single value from the users table based on a specified column and value
    def get(self, column1, column2, value):
        # Get a database connection and select the value from the users table based on the specified column and value
        conn, cur = self.get_db_connection()
        command = f'''
            select {column1} from users where {column2}=%s
            '''.format(column1, column2)
        
        cur.execute(command, (value,))
        data = cur.fetchone()
        # If data is found, close the connection and return the first value in the data tuple
        if data:
            cur.close()
            conn.close()
            return data[0] 
