from flask import Flask, request, jsonify
import json
import logging
import flask.json


from src import log_init, db_util
import decimal

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = MyJSONEncoder
with open('./config.json') as f:
    config = json.load(f)
app.config.update(config)

error_msg = {'message': 'error'}


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/restaurant', methods=['OPTIONS'])
def restaurant_count():
    log = logging.getLogger('restaurant_count')
    try:
        statement = 'select count(*) from restaurant'
        log.info('statement:' + statement)
        conn = db_util.db_get_conn(config, log)
        cur = db_util.db_execute(conn, statement, log)
        count = dict(list(cur.fetchall())[0])
        log.info(str(count))
        cur.close()
        return jsonify(count)
    except:
        log.info("Catch an exception.", exc_info=True)
        return jsonify(error_msg)

@app.route('/restaurant', methods=['GET'])
def get_restaurant():
    try:
        log = logging.getLogger('get_restaurant')
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        statement = 'select * from restaurant offset ' + offset + ' limit ' + limit
        log.info('statement:' + statement)
        conn = db_util.db_get_conn(config, log)
        cur = db_util.db_execute(conn, statement, log)
        rows = list(cur.fetchall())
        data = []
        for row in rows:
            row = dict(row)
            data.append(row)
        log.info('data:' + str(data))
        return jsonify({'data': data})
    except:
        log.info("Catch an exception.", exc_info=True)
        return jsonify(error_msg)

if __name__ == '__main__':
    # get all route endpoints
    endpoints = []
    for rule in app.url_map.iter_rules():
        endpoints.append(rule.endpoint)
    endpoints.remove('static')
    # init all log setting
    log_init.init_log(endpoints, r"../log/")
    run_port = 5000
    if app.config.get('API_PORT'):
        run_port = app.config.get('API_PORT')
    app.run(threaded=True, host='0.0.0.0', port=run_port, debug=True)
