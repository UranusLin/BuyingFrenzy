import json
import logging
from src import log_init, db_util
from datetime import datetime
from dateutil import parser
import os

weekend = {
    'Mon': '1',
    'Tues': '2',
    'Wed': '3',
    'Weds': '3',
    'Thurs': '4',
    'Thu': '4',
    'Fri': '5',
    'Sat': '6',
    'Sun': '7'
}

weekend_list = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']

def til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close):
    if int(weekend.get(first_day)) > int(weekend.get(end_day)):
        # for cross week
        count = int(weekend.get(first_day))
        a = []
        while count != int(weekend.get(end_day)) + 1:
            data = (weekend_list[count - 1], open_time_open, open_time_close, str(restaurant_id))
            insert_data.append(data)
            a.append(data)
            if count == 7:
                count = 1
            else:
                count += 1
    else:
        for i in range(int(weekend.get(first_day)), int(weekend.get(end_day)) + 1):
            data = (str(weekend_list[i - 1]), open_time_open, open_time_close, str(restaurant_id))
            insert_data.append(data)

def init_db_table(config, conn, log):
    table_list = config.get('DB_TABLE')
    cur = conn.cursor()
    for table in table_list:
        log.info('create ' + table + ' if not in DB')
        if config.get(table + '_CREATE'):
            # first drop table in db
            cur.execute('drop table ' + table)
            # create table
            cur.execute(config.get(table + '_CREATE'))
            conn.commit()
            log.info('table create')

def init_db_restaurant(conn, log):
    with open("../data/restaurant_with_menu.json", 'r') as load_f:
        load_dict = json.load(load_f)

    for restaurant in load_dict:
        # insert restaurant table
        statement = '(restaurantname, cashbalance) VALUES (%s, %s) RETURNING id'
        data = (restaurant.get('restaurantName'), str(restaurant.get('cashBalance')))
        cur = db_util.db_insert(conn, 'restaurant', statement, data, log)
        restaurant_id = int(cur.fetchall()[0].get('id'))
        cur.close()
        menu_list = restaurant.get('menu')
        insert_data = []
        # insert menu table
        for menu in menu_list:
            data = (menu.get('dishName'), str(menu.get('price')), str(restaurant_id))
            insert_data.append(data)
        cur = conn.cursor()
        statement = ' INSERT INTO menu (dishname, price, restaurant_id) VALUES (%s, %s, %s)'
        cur.executemany(statement, insert_data)
        cur.close()
        conn.commit()
        # insert openhours table
        open_days = restaurant.get('openingHours').split('/')
        cur = conn.cursor()
        statement = 'INSERT INTO openhours (week, open, close, restaurant_id) VALUES (%s, %s, %s, %s)'
        insert_data = []
        for day in open_days:
            day = list(filter(None, day.split(' ')))
            open_time = day[-5:]
            week = day[:-5]
            open_time_open = parser_time_hh_mm(''.join(open_time).split('-')[0])
            open_time_close = parser_time_hh_mm(''.join(open_time).split('-')[1])

            if len(week) == 1:
                if weekend.get(week[0]):
                    #  insert one day
                    data = (str(weekend_list[int(weekend.get(week[0])) - 1]), open_time_open, open_time_close, str(restaurant_id))
                    insert_data.append(data)
                else:
                    # day til day
                    day_list = week[0].split('-')
                    first_day = day_list[0]
                    end_day = day_list[1]
                    for i in range(int(weekend.get(first_day)), int(weekend.get(end_day)) + 1):
                        data = (str(weekend_list[i - 1]), open_time_open, open_time_close, str(restaurant_id))
                        insert_data.append(data)
            elif len(week) == 2:
                if len(week[0].split(',')) == 2:
                    first_day = weekend.get(week[0].split(',')[0])
                    if first_day:
                        data = (weekend_list[int(first_day) - 1], open_time_open, open_time_close, str(restaurant_id))
                        insert_data.append(data)
                        if weekend.get(week[1]):
                            data = (weekend_list[int(weekend.get(week[1])) - 1], open_time_open, open_time_close, str(restaurant_id))
                            insert_data.append(data)
                        else:
                            day_list = week[1].split('-')
                            first_day = day_list[0]
                            end_day = day_list[1]
                            for i in range(int(weekend.get(first_day)), int(weekend.get(end_day)) + 1):
                                data = (str(weekend_list[i - 1]), open_time_open, open_time_close, str(restaurant_id))
                                insert_data.append(data)
                    else:
                        day_list = week[0].split(',')[0].split('-')
                        first_day = day_list[0]
                        end_day = day_list[1]
                        for i in range(int(weekend.get(first_day)), int(weekend.get(end_day)) + 1):
                            data = (str(weekend_list[i - 1]), open_time_open, open_time_close, str(restaurant_id))
                            insert_data.append(data)
                        data = (weekend_list[int(weekend.get(week[1])) - 1], open_time_open, open_time_close, str(restaurant_id))
                        insert_data.append(data)
            elif len(week) == 3:
                if week[1] == '-':
                    first_day = week[0]
                    end_day = week[2]
                    til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)
                else:
                    for we in week:
                        if weekend.get(we.split(',')[0]):
                            data = (weekend_list[int(weekend.get(we.split(',')[0])) - 1], open_time_open, open_time_close, str(restaurant_id))
                            insert_data.append(data)
            elif len(week) == 4:
                if len(week[0].split(',')) == 2:
                    first_day = weekend.get(week[0].split(',')[0])
                    if first_day:
                        data = (weekend_list[int(first_day) - 1], open_time_open, open_time_close, str(restaurant_id))
                        insert_data.append(data)
                        first_day = week[1]
                        end_day = week[3]
                        for i in range(int(weekend.get(first_day)), int(weekend.get(end_day)) + 1):
                            data = (str(weekend_list[i - 1]), open_time_open, open_time_close, str(restaurant_id))
                            insert_data.append(data)
                else:
                    first_day = week[0]
                    end_day = week[2].split(',')[0]
                    til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)

                    data = (str(weekend_list[int(weekend.get(week[3])) - 1]), open_time_open, open_time_close, str(restaurant_id))
                    insert_data.append(data)
            elif len(week) == 5:
                if week[1] == '-':
                    first_day = week[0]
                    end_day = week[2].split(',')[0]
                    til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)
                    data = (str(weekend_list[int(weekend.get(week[3].split(',')[0])) - 1]), open_time_open, open_time_close, str(restaurant_id))
                    insert_data.append(data)
                    data = (str(weekend_list[int(weekend.get(week[4])) - 1]), open_time_open, open_time_close, str(restaurant_id))
                    insert_data.append(data)
                elif week[2] == '-':
                    first_day = week[1]
                    end_day = week[3].split(',')[0]
                    til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)
                    data = (str(weekend_list[int(weekend.get(week[0].split(',')[0])) - 1]), open_time_open, open_time_close,
                            str(restaurant_id))
                    insert_data.append(data)
                    data = (str(weekend_list[int(weekend.get(week[4])) - 1]), open_time_open, open_time_close, str(restaurant_id))
                    insert_data.append(data)
                else:
                    first_day = week[2]
                    end_day = week[4]
                    til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)
                    data = (str(weekend_list[int(weekend.get(week[0].split(',')[0])) - 1]), open_time_open, open_time_close,
                            str(restaurant_id))
                    insert_data.append(data)
                    data = (str(weekend_list[int(weekend.get(week[1].split(',')[0])) - 1]), open_time_open, open_time_close, str(restaurant_id))
                    insert_data.append(data)
            else:
                first_day = week[0]
                end_day = week[2].split(',')[0]
                til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)
                first_day = week[3]
                end_day = week[5]
                til_days(first_day, end_day, open_time, restaurant_id, insert_data, open_time_open, open_time_close)
        cur.executemany(statement, insert_data)
        cur.close()
        conn.commit()

def parser_time_hh_mm(time):
    return datetime.strftime(parser.parse(time), '%H:%M')

def init_db_users(conn, log):
    with open("../data/users_with_purchase_history.json", 'r') as load_f:
        load_dict = json.load(load_f)

    for user in load_dict:
        statement = '(id, name, cashbalance) VALUES (%s, %s, %s) RETURNING id'
        data = (str(user.get('id')), str(user.get('name')), str(user.get('cashBalance')))
        cur = db_util.db_insert(conn, 'users', statement, data, log)
        user_id = cur.fetchall()[0]
        cur.close()
        purchaseHistory = user.get('purchaseHistory')
        insert_data = []
        for h in purchaseHistory:
            statement = ' where restaurantname = %s'
            data = [str(h.get('restaurantName'))]
            cur = db_util.db_query(conn, 'restaurant', statement, log, data)
            restaurant_id = cur.fetchall()[0][0]
            cur.close()
            statement = ' where dishname = %s and restaurant_id = %s '
            data = [str(h.get('dishName')), str(restaurant_id)]
            cur = db_util.db_query(conn, 'menu', statement, log, data)
            menu_id = cur.fetchall()[0][0]
            cur.close()
            transactionDate = datetime.timestamp(datetime.strptime(str(h.get('transactionDate')).strip(), '%m/%d/%Y %H:%M %p'))
            data = (str(menu_id), str(restaurant_id), str(h.get('transactionAmount')), str(int(transactionDate)), str(user_id))
            insert_data.append(data)
        statement = ' INSERT INTO purchasehistory (menu_id, restaurant_id, transactionamount, transactiondate, user_id) VALUES (%s, %s, %s, %s, %s)'
        cur = conn.cursor()
        cur.executemany(statement, insert_data)
        cur.close()
        conn.commit()

if __name__ == "__main__":
    try:
        log_init.init_log(["data_init"], r"../log/")
        log = logging.getLogger('data_init')

        with open("./config.json", 'r') as load_f:
            config = json.load(load_f)

        conn = db_util.db_get_conn(config, log)
        # init db table
        init_db_table(config, conn, log)
        # init restaurant db
        init_db_restaurant(conn, log)
        # init users db
        init_db_users(conn, log)
        log.info('init success')

    except:
        log.info("Catch an exception.", exc_info=True)
    finally:
        if conn:
            conn.close()
