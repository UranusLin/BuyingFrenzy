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