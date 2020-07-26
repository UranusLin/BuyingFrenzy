from datetime import datetime
from dateutil import parser
from src import db_util


def query_db(limit, offset, statement, log, config, query_data=None):
    if limit and offset:
        statement = statement + ' offset ' + offset + ' limit ' + limit
    log.info('statement:' + statement)
    conn = db_util.db_get_conn(config, log)
    if query_data:
        cur = db_util.db_execute(conn, statement, log, query_data)
    else:
        cur = db_util.db_execute(conn, statement, log)
    rows = list(cur.fetchall())
    data = []
    for row in rows:
        row = dict(row)
        if row.get('open'):
            row['open'] = datetime.strftime(parser.parse(str(row.get('open'))), '%H:%M %p')
        if row.get('close'):
            row['close'] = datetime.strftime(parser.parse(str(row.get('close'))), '%H:%M %p')
        data.append(row)
    return data
