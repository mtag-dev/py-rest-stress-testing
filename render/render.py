import csv
import datetime as dt
import re
import statistics as st
from collections import namedtuple
from pathlib import Path

import jinja2


NOW = dt.datetime.utcnow()
BASEDIR = Path(__file__).parent.parent
FRAMEWORKS = BASEDIR / 'frameworks'
README = Path(BASEDIR / 'README.md')
README_TEMPLATE = jinja2.Template((BASEDIR / 'render/README.md').read_text())
# PAGES_HOME = Path(BASEDIR / 'docs/index.md')
PAGES_HOME_TEMPLATE = jinja2.Template((BASEDIR / 'render/pages/index.md').read_text())
# PAGES_RESULTS = Path(BASEDIR / f"docs/_posts/{ NOW.strftime('%Y-%m-%d') }-results.md")
PAGES_RESULTS_TEMPLATE = jinja2.Template((BASEDIR / 'render/pages/results.md').read_text())

Result = namedtuple('Result', ['name', 'path', 'version', 'req', 'lt50', 'lt75', 'lt90', 'lt_avg', 'es', 'er', 'et'])

results = {
    "res_userinfo_raw": Path(BASEDIR / 'results/userinfo-raw.csv'),
    "res_userinfo_dataclass": Path(BASEDIR / 'results/userinfo-dataclasses.csv'),
    "res_sprint_raw": Path(BASEDIR / 'results/sprint-raw.csv'),
    "res_sprint_dataclass": Path(BASEDIR / 'results/sprint-dataclasses.csv'),
    "res_create_task_raw": Path(BASEDIR / 'results/create-task-raw.csv'),
    "res_create_task_dataclass": Path(BASEDIR / 'results/create-task-dataclasses.csv'),
    "res_update_task_raw": Path(BASEDIR / 'results/update-task-raw.csv'),
    "res_update_task_dataclass": Path(BASEDIR / 'results/update-task-dataclasses.csv'),
}


framework_pathes = {"squall": "https://pypi.org/project/python-squall/",
                    "muffin": "https://pypi.org/project/muffin/",
                    "falcon": "https://pypi.org/project/falcon/",
                    "blacksheep": "https://pypi.org/project/blacksheep/",
                    "emmett": "https://pypi.org/project/emmett/",
                    "starlette": "https://pypi.org/project/starlette/",
                    "baize": "https://pypi.org/project/baize/",
                    "sanic": "https://pypi.org/project/sanic/",
                    "aiohttp": "https://pypi.org/project/aiohttp/",
                    "fastapi": "https://pypi.org/project/fastapi/",
                    "quart": "https://pypi.org/project/quart/"}


def render():
    """Load CSV Results and render it into README."""
    dataset = {}

    for scenario, source in results.items():
        with open(source) as csvfile:
            dataset[scenario] = [
                Result(name, get_path(name), parse_version(name), round(int(req) / 15), *row)
                for name, req, *row in csv.reader(csvfile)]

    ctx = dict(
        now=NOW,
    )
    for scenario, data in dataset.items():
        ctx[scenario] = sorted(data, key=lambda res: res.req, reverse=True)

    # Render README
    render_template(README_TEMPLATE, README, **ctx)

    # Render pages
    # render_template(PAGES_HOME_TEMPLATE, PAGES_HOME, **ctx)
    # render_template(PAGES_RESULTS_TEMPLATE, PAGES_RESULTS, **ctx)


def parse_version(name):
    fw_name = name.split('-')[0]
    requirements = (FRAMEWORKS / fw_name / 'requirements.txt').read_text()
    version = re.match(f"^\S*{fw_name}[^=]*==\s*(.*)\s*$", requirements, re.MULTILINE)  # noqa
    return version and version.group(1) or ''


def get_path(name):
    fw_name = name.split('-')[0]
    return framework_pathes.get(fw_name)


def render_template(template, target, **ctx):
    with open(target, 'w') as target:
        target.write(template.render(**ctx))


if __name__ == '__main__':
    render()

# pylama:ignore=D
