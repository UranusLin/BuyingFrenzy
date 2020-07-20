import psycopg2
from psycopg2.extras import RealDictCursor

from src import utils


# Create
def db_insert(conn, table_name, statement, data, log):
    try:
        insert_statement = 'INSERT INTO ' + table_name + ' ' + statement
        return db_execute(conn, insert_statement, log, data)
    except:
        log.error("Catch an exception.", exc_info=True)
        return None

# Read
def db_query(conn, table_name, statement, log, data):
    try:
        select_statement = 'SELECT * ' + ' FROM ' + table_name + statement
        return db_execute(conn, select_statement, log, data)
    except:
        log.error("Catch an exception.", exc_info=True)
        return None

# Update
def db_update(conn, table_name, statement, log):
    try:
        statement = 'UPDATE ' + table_name + ' SET ' + statement
        return db_execute(conn, statement, log)
    except:
        log.error("Catch an exception.", exc_info=True)
        return None

# Delete
def db_delete(conn, table_name, statement, log):
    try:
        statement = 'DELETE FROM ' + table_name + ' WHERE ' + statement
        return db_execute(conn, statement, log)
    except:
        log.error("Catch an exception.", exc_info=True)
        return None

# get connection
def db_get_conn(config, log):
    try:
        return psycopg2.connect(database=config.get('database'), user=config.get('user'), password=config.get('password'), host=config.get('host'), port=config.get('port'))
    except:
        log.error("Catch an exception.", exc_info=True)
        return utils.jsonifym({'message': 'error'})

# execute sql
def db_execute(conn, statement, log, data=False):
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if data:
            cur.execute(statement, data)
        else:
            cur.execute(statement)
        conn.commit()
        return cur
    except:
        log.error("Catch an exception.", exc_info=True)
        return None
