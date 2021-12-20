# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-12-20
#### Original benchmark: https://klen.github.io/py-frameworks-bench/

[![benchmarks](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/benchmarks.yml)
[![tests](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/tests.yml/badge.svg)](https://github.com/mtag-dev/py-rest-stress-testing/actions/workflows/tests.yml)

----------

We aim to create a tool for technical decision-making.

This is a benchmark for modern ASGI micro-frameworks. 
Designed to be not one more "Hello world" benchmark, but cover some real-like 
scenarios instead. Doesn't provide composite scoring, drills down instead.

To be data source agnostic (API, DB, etc.) framework provides thread-safe async 
dummy pool with configurable size and data retrieving latency. Because of our 
target is benchmark web-frameworks itself, this feature by default configured 
with default pool size `10` and latency `1ms` (emulates very fast data source, 
like Redis.)

Through polls, we have found out that AVG mature service contains ~30 endpoints. 
So during a time, routing performance can drop. We cover this by adding 30 more 
dynamic endpoints with different methods. These endpoints are just present for 
routing cycle load.

This benchmark doesn't provide load tests for different ASGI servers. All tests 
(except AioHTTP) runs on the Uvicorn.

Doesn't contain benchmarks for OAuth 2.0/OIDC/JWT features. 
This is because we pretty sure that these features should be a part of API-Gateway 
and not in end service itself.

Further development implies adding scenarios from different domains. 
For now, it is only issue tracker as example

## Table of contents

* [The Methodic](#the-methodic)
* [The Results](#the-results-2021-12-20)
* [JSON response without schema](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * [PUT: Update task](#update-task-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * [PUT: Update task](#update-task-dataclass)
    * [GET: Sprint board](#sprint-dataclass)


## The Methodic

The benchmark runs as a [Github Action](https://github.com/features/actions).
According to the [github
documentation](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
the hardware specification for the runs is:

* 2-core vCPU (Intel® Xeon® Platinum 8272CL (Cascade Lake), Intel® Xeon® 8171M 2.1GHz (Skylake))
* 7 GB of RAM memory
* 14 GB of SSD disk space
* OS Ubuntu 20.04

[ASGI](https://asgi.readthedocs.io/en/latest/) apps are running from docker using the gunicorn/uvicorn command:

    gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 app:app

Applications' source code can be found
[here](https://github.com/mtag-dev/py-rest-stress-testing/tree/master/frameworks).

Results received with WRK utility using the params:

    wrk -d15s -t4 -c32 [URL]

The "Issue tracker" suite has a four kind of tests:
- getting user information
- create task
- update task
- board with short information with 100 issues on it

You can find test data [here](https://github.com/mtag-dev/py-rest-stress-testing/tree/master/fixtures).

## The Results (2021-12-20)

### JSON response without schema

<h3 id="userinfo-raw"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22blacksheep-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5425%2C5160%2C5082%2C5064%2C4723%2C4473%2C4321%2C3693%2C2809%2C2166%2C2013%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 5425 | 11.79 | 13.01 | 11.99
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 5160 | 12.21 | 13.74 | 12.52
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 5082 | 12.49 | 13.77 | 12.84
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 5064 | 12.77 | 13.96 | 12.70
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 4723 | 13.71 | 15.16 | 13.57
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 4473 | 13.84 | 15.75 | 14.54
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 4321 | 14.72 | 16.39 | 14.83
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3693 | 16.61 | 18.79 | 17.47
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2809 | 21.62 | 25.44 | 22.81
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2166 | 29.27 | 30.02 | 29.53
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2013 | 30.45 | 33.65 | 31.76


</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22sanic-raw%22%2C%22emmett-raw%22%2C%22falcon-raw%22%2C%22baize-raw%22%2C%22blacksheep-raw%22%2C%22starlette-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3564%2C2643%2C2112%2C2047%2C1847%2C1640%2C1611%2C1601%2C1234%2C1034%2C213%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 3564 | 16.75 | 20.30 | 17.99
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 2643 | 22.79 | 28.17 | 24.17
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 2112 | 28.95 | 34.73 | 30.26
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 2047 | 29.16 | 35.75 | 31.17
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 1847 | 32.66 | 40.82 | 34.57
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 1640 | 38.12 | 44.74 | 39.03
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 1611 | 37.81 | 46.38 | 39.66
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 1601 | 39.03 | 46.13 | 39.88
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1234 | 51.19 | 53.16 | 51.78
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1034 | 61.55 | 67.13 | 61.75
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 213 | 298.01 | 355.90 | 297.95


</details>


<h3 id="create-task-raw"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-raw%22%2C%22muffin-raw%22%2C%22falcon-raw%22%2C%22blacksheep-raw%22%2C%22emmett-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22sanic-raw%22%2C%22quart-raw%22%2C%22aiohttp-raw%22%2C%22fastapi-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4866%2C4543%2C4513%2C4080%2C3708%2C3533%2C3498%2C3398%2C1858%2C1855%2C1538%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4866 | 12.99 | 14.46 | 13.25
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4543 | 14.32 | 15.66 | 14.11
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4513 | 14.22 | 15.75 | 14.17
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4080 | 15.39 | 17.09 | 15.84
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3708 | 16.48 | 18.46 | 17.72
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3533 | 17.61 | 19.75 | 18.09
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3498 | 18.20 | 19.17 | 18.27
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3398 | 17.78 | 20.57 | 19.00
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 1858 | 32.95 | 37.22 | 34.37
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 1855 | 34.37 | 35.17 | 34.46
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 1538 | 40.99 | 46.71 | 41.51


</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22falcon-raw%22%2C%22squall-raw%22%2C%22blacksheep-raw%22%2C%22muffin-raw%22%2C%22starlette-raw%22%2C%22baize-raw%22%2C%22emmett-raw%22%2C%22sanic-raw%22%2C%22fastapi-raw%22%2C%22aiohttp-raw%22%2C%22quart-raw%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4979%2C4889%2C4865%2C4790%2C3948%2C3945%2C3852%2C3583%2C2416%2C2339%2C2094%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [falcon-raw](https://pypi.org/project/falcon/) `3.0.1` | 4979 | 12.76 | 14.13 | 12.86
| [squall-raw](https://pypi.org/project/python-squall/) `0.2.1` | 4889 | 12.76 | 14.37 | 13.25
| [blacksheep-raw](https://pypi.org/project/blacksheep/) `1.2.2` | 4865 | 12.89 | 14.42 | 13.35
| [muffin-raw](https://pypi.org/project/muffin/) `0.86.3` | 4790 | 13.22 | 14.73 | 13.40
| [starlette-raw](https://pypi.org/project/starlette/) `0.17.1` | 3948 | 16.04 | 17.47 | 16.19
| [baize-raw](https://pypi.org/project/baize/) `0.14.1` | 3945 | 16.01 | 16.79 | 16.19
| [emmett-raw](https://pypi.org/project/emmett/) `2.3.2` | 3852 | 15.62 | 17.68 | 17.18
| [sanic-raw](https://pypi.org/project/sanic/) `21.9.3` | 3583 | 16.77 | 19.45 | 18.03
| [fastapi-raw](https://pypi.org/project/fastapi/) `0.70.1` | 2416 | 25.56 | 30.13 | 26.47
| [aiohttp-raw](https://pypi.org/project/aiohttp/) `3.8.1` | 2339 | 26.98 | 27.73 | 27.35
| [quart-raw](https://pypi.org/project/quart/) `0.16.2` | 2094 | 28.99 | 32.20 | 30.51


</details>

### JSON response using schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B5010%2C3484%2C2384%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 5010 | 12.71 | 14.18 | 12.90
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3484 | 17.54 | 19.92 | 18.37
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2384 | 25.93 | 29.88 | 26.86


</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B826%2C200%2C138%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 826 | 76.63 | 92.00 | 77.37
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 200 | 325.37 | 354.93 | 316.58
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 138 | 440.94 | 536.84 | 456.65


</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3117%2C1561%2C1179%5D%7D%5D%7D%7D' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 3117 | 19.13 | 22.80 | 20.50
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 1561 | 40.31 | 45.83 | 40.89
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 1179 | 52.68 | 60.88 | 54.19


</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclasses%22%2C%22blacksheep-dataclasses%22%2C%22fastapi-dataclasses%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4840%2C3802%2C2219%5D%7D%5D%7D%7D' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclasses](https://pypi.org/project/python-squall/) `0.2.1` | 4840 | 13.16 | 14.57 | 13.30
| [blacksheep-dataclasses](https://pypi.org/project/blacksheep/) `1.2.2` | 3802 | 16.30 | 18.25 | 16.88
| [fastapi-dataclasses](https://pypi.org/project/fastapi/) `0.70.1` | 2219 | 27.58 | 32.55 | 28.78


</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)