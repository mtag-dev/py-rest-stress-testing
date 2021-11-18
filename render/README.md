# ASGI Python Frameworks load testing

https://github.com/mtag-dev/py-rest-stress-testing
----------
#### Updated: {{ now.strftime('%Y-%m-%d') }}
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
* [The Results](#the-results-{{ now.strftime('%Y-%m-%d')  }})
* [JSON response from primitives](#json-response-from-primitives)
    * [GET: User info](#userinfo-raw)
    * [POST: Create task](#create-task-raw)
    * [PUT: Update task](#update-task-raw)
    * [GET: Sprint board](#sprint-raw)
* [JSON response using Dataclasses schema](#json-response-using-dataclasses-schema)
    * [GET: User info](#userinfo-dataclass)
    * [POST: Create task](#create-task-dataclass)
    * [PUT: Update task](#update-task-dataclass)
    * [GET: Sprint board](#sprint-dataclass)
* [JSON response using Pydantic schema](#json-response-using-pydantic-schema)
    * [GET: User info](#userinfo-pydantic)
    * [POST: Create task](#create-task-pydantic)
    * [PUT: Update task](#update-task-pydantic)
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

## The Results ({{ now.strftime('%Y-%m-%d') }})

### JSON response from primitives

<h3 id="userinfo-raw"> User info (GET) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_userinfo_raw|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_userinfo_raw|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Get user information and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_userinfo_raw -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>


<h3 id="sprint-raw"> Sprint issues (GET) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_sprint_raw|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_sprint_raw|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Get sprint tickets overview and return using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_sprint_raw -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>


<h3 id="create-task-raw"> Create task (POST) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_create_task_raw|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_create_task_raw|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Create task object using default payload and return created object using direct serialisation from Python primitives to JSON. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_create_task_raw -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>

<h3 id="update-task-raw"> Update task (PUT) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_update_task_raw|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_update_task_raw|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Update task object using default payload. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_update_task_raw -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>

### JSON response using Dataclasses schema

<h3 id="userinfo-dataclass"> User info (GET) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_userinfo_dataclass|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_userinfo_dataclass|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Get user information and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_userinfo_dataclass -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>


<h3 id="sprint-dataclass"> Sprint issues (GET) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_sprint_dataclass|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_sprint_dataclass|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Get sprint tickets overview and return using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_sprint_dataclass -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>


<h3 id="create-task-dataclass"> Create task (POST) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_create_task_dataclass|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_create_task_dataclass|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Create task object using default payload and return created object using dataclasses, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_create_task_dataclass -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>

<h3 id="update-task-dataclass"> Update task (PUT) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_update_task_dataclass|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_update_task_dataclass|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_update_task_dataclass -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>

### JSON response using Pydantic schema

<h3 id="userinfo-pydantic"> User info (GET) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_userinfo_pydantic|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_userinfo_pydantic|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Get user information and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_userinfo_pydantic -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>


<h3 id="sprint-pydantic"> Sprint issues (GET) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_sprint_pydantic|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_sprint_pydantic|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Get sprint tickets overview and return using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_sprint_pydantic -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>

<h3 id="create-task-pydantic"> Create task (POST) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_create_task_pydantic|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_create_task_pydantic|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Create task object using default payload and return created object using pydantic, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_create_task_pydantic -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>

<h3 id="update-task-pydantic"> Update task (PUT) </h3>

{% set chart_data = '{type:"bar",data:{labels:["' + res_update_task_pydantic|join("\",\"", attribute="name") + '"],datasets:[{label:"req/s",data:[' + res_update_task_pydantic|join(",", attribute="req") + ']}]}}' %}

<img src='https://quickchart.io/chart?width=800&height=400&c={{ chart_data|urlencode }}' />

<details open>
<summary> Update task object using default payload, no extra validation. </summary>

Sorted by max req/s

| Framework | Requests/sec | Latency 50% (ms) | Latency 75% (ms) | Latency Avg (ms) |
| --------- | -----------: | ---------------: | ---------------: | ---------------: |
{% for res in res_update_task_pydantic -%}
| [{{ res.name }}](https://pypi.org/project/{{ res.name }}/) `{{ res.version }}` | {{ res.req }} | {{ res.lt50 }} | {{ res.lt75 }} | {{ res.lt_avg }}
{% endfor %}

</details>


## Conclusion

Nothing here, just some measures for you.

## License

Licensed under a MIT license (See LICENSE file)
