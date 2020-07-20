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

API document


/restaurant
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
```


This project was bootstrapped with [Flask](https://palletsprojects.com/p/flask/).