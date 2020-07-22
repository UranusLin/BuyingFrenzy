from flask import Flask, request, jsonify
import json
import logging
import flask.json
from datetime import datetime
from dateutil import parser

from src import log_init, db_util
import decimal

from src.utils import query_db


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

weekend_list = ['Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat']

@app.route('/restaurant', methods=['OPTIONS'])
def restaurant_count():
    conn = None
    query_data = None
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
    finally:
        if conn:
            conn.close()

@app.route('/restaurant', methods=['GET'])
def get_restaurant():
    try:
        conn = None
        query_data = None
        log = logging.getLogger('get_restaurant')
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        date = request.args.get('date', default=None)
        time = request.args.get('time', default=None)
        week = request.args.get('week', default=None)

        if date and week:
            log.error('two query week and date')
            error_msg['code'] = '102'
            error_msg['message'] = 'two query week and date'
            return jsonify({'data': error_msg})
        if time and not (not date or not week):
            log.error('not date just time')
            error_msg['code'] = '101'
            error_msg['message'] = 'just time no date'
            return jsonify({'data': error_msg})

        statement = 'select * from restaurant '
        if date:
            try:
                week = datetime.strftime(parser.parse(date), '%w')
                statement = statement + ' JOIN openhours ON (restaurant.id = openhours.restaurant_id) where openhours.week = %s '
                query_data = (weekend_list[int(week)],)
                if time:
                    time = datetime.strftime(parser.parse(time), '%H%M')
                    statement = statement + ' and open <= %s'
                    l = list(query_data)
                    l.append(time)
                    query_data = tuple(l)
            except:
                log.info("Catch an exception.", exc_info=True)
                error_msg['message'] = 'wrong date'
                error_msg['code'] = '99'
                return jsonify(error_msg)
        if week:
            try:
                statement = statement + ' JOIN openhours ON (restaurant.id = openhours.restaurant_id) where openhours.week = %s '
                query_data = (week,)
                if time:
                    time = datetime.strftime(parser.parse(time), '%H%M')
                    statement = statement + ' and open <= %s'
                    l = list(query_data)
                    l.append(time)
                    query_data = tuple(l)
            except:
                log.info("Catch an exception.", exc_info=True)
                error_msg['message'] = 'wrong date'
                error_msg['code'] = '99'
                return jsonify(error_msg)

        data = query_db(limit, offset, statement, log, config, query_data)
        log.info('data:' + str(data))
        return jsonify({'data': data})
    except:
        log.info("Catch an exception.", exc_info=True)
        return jsonify(error_msg)
    finally:
        if conn:
            conn.close()

@app.route('/restaurant/hour', methods=['GET'])
def get_restaurant_hour():
    try:
        conn = None
        query_data = None
        log = logging.getLogger('get_restaurant_hour')
        query_type = request.args.get('query_type', default=None)
        date_type = request.args.get('date_type', default=None)
        hour = request.args.get('hour', default=None)
        offset = request.args.get('offset', default=None)
        limit = request.args.get('limit', default=None)
        wrong = False
        if not query_type or not date_type or not hour:
            wrong = True
        if query_type != 'more' and query_type != 'less':
            wrong = True
        if date_type != 'day' and date_type != 'week':
            wrong = True
        if not isinstance(int(hour), int):
            wrong = True
        if wrong:
            log.error('wrong params')
            error_msg['code'] = '103'
            error_msg['message'] = 'wrong params'
            return jsonify({'data': error_msg})
        statement = 'select * from restaurant '
        if date_type == 'day':
            if query_type == 'more':
                statement = statement + ' JOIN openhours ON (restaurant.id = openhours.restaurant_id) where (open-close) > interval %s '
            else:
                statement = statement + ' JOIN openhours ON (restaurant.id = openhours.restaurant_id) where (open-close) < interval %s '
            hour = hour + ' hour'
            query_data = (hour,)
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
                row['open'] = datetime.strftime(parser.parse(str(row.get('open'))), '%H:%M %p')
                row['close'] = datetime.strftime(parser.parse(str(row.get('close'))), '%H:%M %p')
                data.append(row)
            log.info('data:' + str(data))
            return jsonify({'data': data})

    except:
        log.info("Catch an exception.", exc_info=True)
        return jsonify(error_msg)
    finally:
        if conn:
            conn.close()

@app.route('/dishes/price', methods=['GET'])
def get_dishes_price():
    try:
        conn = None
        query_data = None
        log = logging.getLogger('get_dishes_price')
        price_max = request.args.get('price_max', default=None)
        price_min = request.args.get('price_min', default=None)
        sort = request.args.get('sort', default=None)
        sort_type = request.args.get('sort_type', default=None)
        offset = request.args.get('offset', default=None)
        limit = request.args.get('limit', default=None)
        wrong = False
        if not price_max and not price_min:
            wrong = True
        if sort != '1' and sort != '2':
            wrong = True
        if sort_type != 'ASC' and sort_type != 'DESC':
            wrong = True
        if price_max and price_min:
            if (int(price_max) < int(price_min)):
                wrong = True
        if wrong:
            log.error('wrong params')
            error_msg['code'] = '103'
            error_msg['message'] = 'wrong params'
            return jsonify({'data': error_msg})
        statement = 'select menu.dishname, menu.price, restaurant.restaurantname from menu join restaurant on (restaurant.id = menu.restaurant_id) where price '
        if price_max and price_min:
            statement = statement + ' between %s and %s'
            query_data = (price_min, price_max)
        elif price_max:
            statement = statement + ' <= %s'
            query_data = (price_max,)
        else:
            statement = statement + ' >= %s'
            query_data = (price_min,)
        if sort == '1':
            statement = statement + ' ORDER BY price ' + sort_type
        else:
            statement = statement + ' ORDER BY dishname ' + sort_type
        data = query_db(limit, offset, statement, log, config, query_data)
        log.info('data:' + str(data))
        return jsonify({'data': data})
    except:
        log.info("Catch an exception.", exc_info=True)
        return jsonify(error_msg)
    finally:
        if conn:
            conn.close()

@app.route('/dishes/amount', methods=['GET'])
def get_dishes_amount():
    try:
        conn = None
        query_data = None
        log = logging.getLogger('get_dishes_amount')
        price_max = request.args.get('price_max', default=None)
        price_min = request.args.get('price_min', default=None)
        dishes_max = request.args.get('dishes_max', default=None)
        dishes_min = request.args.get('dishes_min', default=None)
        offset = request.args.get('offset', default=None)
        limit = request.args.get('limit', default=None)
        wrong = False
        if not dishes_max and not dishes_min:
                wrong = True
        if dishes_max and dishes_min:
            if (int(dishes_max) < int(dishes_min)):
                wrong = True
        if wrong:
            log.error('wrong params')
            error_msg['code'] = '103'
            error_msg['message'] = 'wrong params'
            return jsonify({'data': error_msg})
        statement = 'select restaurant.restaurantname, count(restaurant_id) from menu join restaurant on (restaurant.id = menu.restaurant_id) '

        if price_max and price_min:
            statement = statement + '  where menu.price between %s and %s'
            query_data = (price_min, price_max)
        elif price_max:
            statement = statement + ' where menu.price <= %s'
            query_data = (price_max,)
        elif price_min:
            query_data = (price_min,)

        statement = statement + ' group by menu.restaurant_id,restaurant.restaurantname   having count(menu.restaurant_id)  '
        if dishes_max and dishes_min:
            statement = statement + ' between %s and %s'
            l = list(query_data)
            l.append(dishes_min)
            l.append(dishes_max)
            query_data = tuple(l)
        elif dishes_max:
            statement = statement + ' <= %s'
            l = list(query_data)
            l.append(dishes_max)
            query_data = tuple(l)
        else:
            statement = statement + ' >= %s'
            l = list(query_data)
            l.append(dishes_max)
            query_data = tuple(l)

        data = query_db(limit, offset, statement, log, config, query_data)
        log.info('data:' + str(data))
        return jsonify({'data': data})
    except:
        log.info("Catch an exception.", exc_info=True)
        return jsonify(error_msg)
    finally:
        if conn:
            conn.close()

#select restaurant.restaurantname, count(restaurant_id) from menu join restaurant on (restaurant.id = menu.restaurant_id)  group by menu.restaurant_id,restaurant.restaurantname   having count(menu.restaurant_id) > 10

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

