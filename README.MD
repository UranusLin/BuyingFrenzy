# BuyingFrenzy

[![Style Guide for Python Code](https://img.shields.io/badge/code%20style-standard-brightgreen.svg?style=flat-square)](https://www.python.org/dev/peps/pep-0008/)

## Development

You need the following tools installed:

* [python](https://www.python.org). version is `3.7`.

### Install Dependencies

Use the command to install dependencies.

```
$ pip install requirements.txt
```

### `python app.py`

Runs the API server in the development mode.<br>
call API in  [http://localhost:5000](http://localhost:5000)

### `Docker build`

Builds [docker](https://www.docker.com) images and run in [docker-compose](https://docs.docker.com/compose/)

## Further Reference

DB model

![image](https://github.com/UranusLin/BuyingFrenzy/blob/master/db_Architecture.png)

API:
use [18.138.124.97:5001](http://18.138.124.97:5001) to test api
```
List all restaurants that are open at a certain datetime
GET /restaurant
Params:
    offset: int
    limit:int
    date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 

List all restaurants that are open on a day of the week, at a certain time
GET /restaurant
Params:
    offset: int
    limit:int
    week: 'Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat' 
    time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 

List all restaurants that are open for more or less than x hours per day or week
GET /restaurant/hour
get open time more or less per week or day
ps. just realize day and have little bug
Params:
    offset: int
    limit:int
    query_type: more/less
    date_type: day/week
    hour: int

List all dishes that are within a price range, sorted by price or alphabetically
GET /dishes/price
get price range in menu
Params:
    offset: int
    limit:int
    price_max: int max price
    price_min: int min price 
    sort: int 1 is sort by price 2 is sort by name

List all restaurants that have more or less than x number of dishes
GET /dishes/amount
get amount from restaurant dishes amount
Params:
    offset: int
    limit:int
    dishes_max: int max dishes
    dishes_min: int min dishes 

List all restaurants that have more or less than x number of dishes within a price range
GET /dishes/amount
get amount from restaurant dishes amount
Params:
    offset: int
    limit:int
    dishes_max: int max dishes
    dishes_min: int min dishes 
    price_max: int max price
    price_min: int min price

Search for restaurants or dishes by name, ranked by relevance to search term
not enough time to develop

The top x users by total transaction amount within a date range
GET /transaction/report
get report about transaction by users or transactionamount
Params:
    offset: int
    limit:int
    type: 1 
    from_date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    from_time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 
    to_date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    to_time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 

The total number and dollar value of transactions that happened 
GET /transaction/report
get report about transaction by users or transactionamount
Params:
    offset: int
    limit:int
    type: 2
    from_date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    from_time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 
    to_date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    to_time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 

Edit restaurant name, dish name, dish price and user name
PATCH /restaurant/[restaurant.id]
patch restaurant data, patch restaurant name or dishname & price
Request:
    restaurantname: string 
    dishname: string
    price: string
    menu_id: int

PATCH /users/[users.id]
patch users name
patch users data
Request:
    name: string

The most popular restaurants by transaction volume, either by number of transactions or transaction dollar value
GET /transaction/rank
get restaurant rank by transaction volume or  transaction dollar value 
Params:
    offset: int
    limit:int
    type: int 1 is transaction volume/ 2 is transaction dollar value

Total number of users who made transactions above or below $v within a date range

Process a user purchasing a dish from a restaurant, handling all relevant data changes in an atomic transaction
POST /transaction/[user.id]/order
users buy dishes 
Request:
    restaurant_id: string
    dish_id: string
```

API document

```
OPTIONS /restaurant
you can use options to get select count
Params:
response:
 {
  "count": 2203
 }

GET /restaurant
to get data by offset and limit to reduce select data for one time
Params:
    offset: int
    limit:int
    date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 
    week: 'Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat' 
response:
    {
      "data": [
        {
          "cashbalance": "4483.84",
          "id": 1,
          "restaurantname": "'Ulu Ocean Grill and Sushi Lounge"
        }
      ]
    }

GET /restaurant/hour
get open time more or less per week or day
Params:
    offset: int
    limit:int
    query_type: more/less
    date_type: day/week
    hour: int

GET /dishes/price
get price range in menu
Params:
    offset: int
    limit:int
    price_max: int max price
    price_min: int min price 
    sort: int 1 is sort by price 2 is sort by name

GET /dishes/amount
get amount from restaurant dishes amount
Params:
    offset: int
    limit:int
    dishes_max: int max dishes
    dishes_min: int min dishes 
    price_max: int max price
    price_min: int min price

GET /transaction/report
get report about transaction by users or transactionamount
Params:
    offset: int
    limit:int
    type: int 1 is user/ 2 is amount
    from_date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    from_time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 
    to_date: certain date ex. 20200720, 2020-07-20, 2020/07/20, 07/20/2020 etc... suppurt
    to_time: time ex. 12:00, 14:00, 08:00 PM, 8AM etc... support 

PATCH /restaurant/[restaurant.id]
patch restaurant data
Request:
    restaurantname: string
    dishname: string
    price: string
    menu_id: int

PATCH /users/[users.id]
patch users data
Request:
    name: string

GET /transaction/rank
get restaurant rank by transaction volume or  transaction dollar value 
Params:
    offset: int
    limit:int
    type: int 1 is transaction volume/ 2 is transaction dollar value 


POST /transaction/[user.id]/order
users buy dishes 
Request:
    restaurant_id: string
    dish_id: string

```

ERROR CODE
````
Code: depiction
99 : wrong date
101: just time no date
102: two query week and date
103: wrong params
````

This project was bootstrapped with [Flask](https://palletsprojects.com/p/flask/).