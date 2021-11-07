# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: 2021-11-07
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
* [The Results](#the-results-2021-11-07)
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

## The Results (2021-11-07)

### JSON response from primitives

<h3 id="userinfo-raw"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22falcon%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22emmett%22%2C%22sanic%22%2C%22squall%22%2C%22fastapi%22%2C%22quart%22%2C%22aiohttp%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B4017%2C3910%2C3827%2C3679%2C3501%2C3344%2C3078%2C3010%2C2551%2C1819%2C1559%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 4017 | 8.24 | 9.05 | 7.96
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 3910 | 8.49 | 9.38 | 8.16
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 3827 | 8.51 | 9.36 | 8.38
| [baize](https://pypi.org/project/baize/) `0.12.1` | 3679 | 9.00 | 9.99 | 8.66
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 3501 | 9.50 | 10.49 | 9.34
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 3344 | 9.54 | 10.71 | 9.65
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 3078 | 10.49 | 11.68 | 10.44
| [squall](https://pypi.org/project/squall/) `` | 3010 | 10.93 | 12.06 | 10.64
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 2551 | 13.03 | 14.30 | 12.59
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1819 | 17.42 | 18.21 | 17.60
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1559 | 20.33 | 21.29 | 20.57


</details>


<h3 id="sprint-raw"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22muffin%22%2C%22emmett%22%2C%22squall%22%2C%22falcon%22%2C%22sanic%22%2C%22blacksheep%22%2C%22baize%22%2C%22starlette%22%2C%22quart%22%2C%22aiohttp%22%2C%22fastapi%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3146%2C2649%2C2448%2C1843%2C1756%2C1683%2C1672%2C1635%2C1103%2C1078%2C192%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [muffin](https://pypi.org/project/muffin/) `0.86.0` | 3146 | 9.22 | 12.01 | 10.16
| [emmett](https://pypi.org/project/emmett/) `2.3.2` | 2649 | 10.90 | 14.04 | 12.11
| [squall](https://pypi.org/project/squall/) `` | 2448 | 11.62 | 15.47 | 13.11
| [falcon](https://pypi.org/project/falcon/) `3.0.1` | 1843 | 15.67 | 20.21 | 17.37
| [sanic](https://pypi.org/project/sanic/) `21.9.1` | 1756 | 16.78 | 21.11 | 18.24
| [blacksheep](https://pypi.org/project/blacksheep/) `1.2.0` | 1683 | 17.23 | 22.48 | 18.98
| [baize](https://pypi.org/project/baize/) `0.12.1` | 1672 | 17.46 | 22.55 | 19.13
| [starlette](https://pypi.org/project/starlette/) `0.16.0` | 1635 | 17.55 | 23.18 | 19.53
| [quart](https://pypi.org/project/quart/) `0.15.1` | 1103 | 28.92 | 30.76 | 28.98
| [aiohttp](https://pypi.org/project/aiohttp/) `3.8.0` | 1078 | 29.32 | 30.34 | 29.68
| [fastapi](https://pypi.org/project/fastapi/) `0.70.0` | 192 | 152.11 | 168.18 | 165.65


</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-dataclass%22%2C%22squall-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3355%2C2712%2C2284%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 3355 | 9.79 | 10.92 | 9.54
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 2712 | 12.24 | 13.45 | 11.83
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 2284 | 14.63 | 15.97 | 14.02


</details>


<h3 id="sprint-dataclass"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-dataclass%22%2C%22blacksheep-dataclass%22%2C%22fastapi-dataclass%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B341%2C205%2C128%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-dataclass](https://pypi.org/project/squall-dataclass/) `` | 341 | 88.08 | 104.80 | 94.33
| [blacksheep-dataclass](https://pypi.org/project/blacksheep-dataclass/) `` | 205 | 145.08 | 161.85 | 155.32
| [fastapi-dataclass](https://pypi.org/project/fastapi-dataclass/) `` | 128 | 225.66 | 259.55 | 247.99


</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22blacksheep-pydantic%22%2C%22squall-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B3026%2C2675%2C2058%5D%7D%5D%7D%7D' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 3026 | 10.90 | 12.05 | 10.55
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 2675 | 12.46 | 13.66 | 11.98
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 2058 | 16.01 | 17.56 | 15.57


</details>


<h3 id="sprint-pydantic"> Sprint issues </h3>



<img src='https://quickchart.io/chart?width=800&height=400&c=%7Btype%3A%22bar%22%2Cdata%3A%7Blabels%3A%5B%22squall-pydantic%22%2C%22blacksheep-pydantic%22%2C%22fastapi-pydantic%22%5D%2Cdatasets%3A%5B%7Blabel%3A%22req/s%22%2Cdata%3A%5B317%2C189%2C86%5D%7D%5D%7D%7D' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
| [squall-pydantic](https://pypi.org/project/squall-pydantic/) `` | 317 | 94.68 | 99.69 | 100.97
| [blacksheep-pydantic](https://pypi.org/project/blacksheep-pydantic/) `` | 189 | 151.97 | 173.00 | 167.73
| [fastapi-pydantic](https://pypi.org/project/fastapi-pydantic/) `` | 86 | 339.83 | 440.52 | 368.23


</details>



## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)