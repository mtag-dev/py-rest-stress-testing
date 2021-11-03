# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-03
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
* [The Results](#the-results-2021-11-03)
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * TODO: [POST: Create issue](#create-raw)
    * TODO: [PATCH: Update issue](#update-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * TODO: [POST: Create issue](#create-dataclass)
    * TODO: [PATCH: Update issue](#update-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * TODO: [POST: Create issue](#create-pydantic)
    * TODO: [PATCH: Update issue](#update-pydantic)
    * [GET: Sprint board](#sprint-pydantic)


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

## The Results (2021-11-03)

### JSON response from primitives

<h3 id="userinfo-raw"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22falcon%22%2C%22blacksheep%22%2C%22emmett%22%2C%22baize%22%2C%22starlette%22%2C%22sanic%22%2C%22fastapi%22%2C%22aiohttp%22%2C%22quart%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4750%2C4564%2C4545%2C4226%2C4160%2C3933%2C3345%2C2799%2C2085%2C1909%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 4750 | 13.15 | 13.88 | 13.47
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 4564 | 13.83 | 14.61 | 14.03
| [blacksheep](https://pypi.org/project/blacksheep/) `1.0.9` | 4545 | 13.95 | 14.68 | 14.07
| [emmett](https://pypi.org/project/emmett/) `2.3.1` | 4226 | 14.96 | 15.41 | 15.16
| [baize](https://pypi.org/project/baize/) `0.12` | 4160 | 15.25 | 15.76 | 15.40
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3933 | 15.96 | 16.55 | 16.27
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3345 | 18.48 | 19.43 | 19.26
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2799 | 22.46 | 23.31 | 22.85
| [aiohttp](https://pypi.org/project/aiohttp/) `3.7.4.post0` | 2085 | 8.06 | 92.14 | 88.10
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1909 | 13.32 | 85.67 | 93.46


</details>


<h3 id="sprint-raw"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22emmett%22%2C%22sanic%22%2C%22falcon%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22aiohttp%22%2C%22quart%22%2C%22fastapi%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3445%2C3056%2C1949%2C1802%2C1621%2C1607%2C1569%2C1221%2C1087%2C219%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3445 | 17.92 | 18.42 | 18.56
| [emmett](https://pypi.org/project/emmett/) `2.3.1` | 3056 | 20.44 | 20.97 | 20.96
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1949 | 31.46 | 32.61 | 32.91
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 1802 | 35.14 | 35.91 | 35.46
| [blacksheep](https://pypi.org/project/blacksheep/) `1.0.9` | 1621 | 38.57 | 40.20 | 39.50
| [baize](https://pypi.org/project/baize/) `0.12` | 1607 | 38.98 | 42.00 | 39.77
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1569 | 40.13 | 41.62 | 40.73
| [aiohttp](https://pypi.org/project/aiohttp/) `3.7.4.post0` | 1221 | 50.05 | 120.54 | 81.83
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1087 | 22.78 | 216.08 | 199.73
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 219 | 294.00 | 299.22 | 290.32


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3729%2C2384%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3729 | 16.97 | 17.47 | 17.16
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2384 | 26.30 | 27.21 | 26.84


</details>


<h3 id="sprint-dataclass"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B224%2C134%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 224 | 271.20 | 298.87 | 283.00
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 134 | 469.46 | 481.18 | 470.29


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3222%2C2114%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 3222 | 19.47 | 19.96 | 19.87
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2114 | 29.97 | 31.00 | 30.48


</details>


<h3 id="sprint-pydantic"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B167%2C87%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 167 | 367.63 | 400.17 | 379.09
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 87 | 692.93 | 788.59 | 721.17


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)