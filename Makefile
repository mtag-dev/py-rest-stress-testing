DATE = $(shell date +'%Y-%m-%d')
VIRTUAL_ENV ?= env

COMMON_WRK = DURATION=15s CONCURRENT=64 THREADS=4

$(VIRTUAL_ENV): frameworks/*/requirements.txt
	@[ -d $(VIRTUAL_ENV) ] || python -m venv $(VIRTUAL_ENV)
	find frameworks | grep requirements | xargs -n1 $(VIRTUAL_ENV)/bin/pip install -r
	touch $(VIRTUAL_ENV)

.PHONY:
benchmark-base:
	docker build $(CURDIR) -t benchmark-base --no-cache

.PHONY:
release:
	git checkout develop
	git pull
	git checkout master
	git pull
	git merge develop
	git checkout develop
	git push origin develop master

APP ?= aiohttp

.PHONY: run
run:
	docker build -f $(CURDIR)/frameworks/Dockerfile -t benchmarks:$(APP) $(CURDIR)/frameworks/$(APP)
	docker run --rm -it --publish 8080:8080 -v $(CURDIR)/frameworks/$(APP):/app --name benchmark benchmarks:$(APP)

.PHONY: clean
clean:
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR)/$(MODULE) -name "__pycache__" | xargs rm -rf
	rm -rf $(CURDIR)/results/*.csv

.PHONY: render
render: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/python render/render.py
	mkdir -p $(CURDIR)/results/$(DATE)
	cp $(CURDIR)/results/*.csv $(CURDIR)/results/$(DATE)/.

.PHONY: tests t
tests t: $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/pip install pytest pytest-aio janus
	$(VIRTUAL_ENV)/bin/pytest frameworks

.PHONY: benchmark-framework-setup
benchmark-framework-setup:
	@echo "\nSetup framework $(FRAMEWORK)\n--------------------"
	@docker build -f $(CURDIR)/frameworks/Dockerfile -t benchmarks:$(FRAMEWORK) $(CURDIR)/frameworks/$(FRAMEWORK)
	@docker run --rm -d --network bench \
			--sysctl net.core.somaxconn=4096 \
			-v `dirname $(CURDIR)`/squall:/squall \
			-v $(CURDIR)/dummy:/app/dummy \
			-v $(CURDIR)/fixtures:/app/fixtures \
			-v $(CURDIR)/frameworks/schema_dataclasses.py:/app/schema_dataclasses.py \
			-v $(CURDIR)/frameworks/schema_pydantic.py:/app/schema_pydantic.py \
			-p 8080:8080 \
			--name benchmark benchmarks:$(FRAMEWORK)

    ifeq ($(FRAMEWORK), squall)
		docker exec benchmark pip install /squall
		@python -c "import time; time.sleep(5)"
    endif
	@python -c "import time; time.sleep(5)"
	@echo "\nSetup finished [$(FRAMEWORK)]\n"

.PHONY: benchmark-framework-teardown
benchmark-framework-teardown:
	@echo "\nTeardown framework $(FRAMEWORK)\n--------------------"
	@docker stop benchmark
	@echo "\nTeardown finished [$(FRAMEWORK)]\n"

.PHONY: benchmark-framework-scenario
benchmark-framework-scenario:
	@echo "\nRun fixture $(FIXTURE) [$(FRAMEWORK) $(SCENARIO)]\n"
	@docker run --rm --network bench \
			-e FRAMEWORK=$(FRAMEWORK) -e FILENAME=$(FILENAME) -e FIXTURE=$(FIXTURE) -e SCENARIO=$(SCENARIO)  \
			-v $(CURDIR)/fixtures:/fixtures \
			-v $(CURDIR)/results:/results \
			-v $(CURDIR)/wrk:/scripts \
			--sysctl net.core.somaxconn=4096 \
			czerasz/wrk-json \
			wrk http://benchmark:8080 -d$(DURATION) -t$(THREADS) -c$(CONCURRENT) -s /scripts/process.lua
	@echo "\nFinish [$(FRAMEWORK) $(SCENARIO)]\n"

benchmark-f: # clean

	@make benchmark-framework-setup FRAMEWORK=$(FRAMEWORK)
### ========== benchmark GET raw ========== ###
	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=raw \
		FILENAME=/results/userinfo-raw.csv \
		FIXTURE=/fixtures/userinfo.json

	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=raw \
		FILENAME=/results/sprint-raw.csv \
		FIXTURE=/fixtures/sprint.json

ifeq ($(FRAMEWORK),$(filter $(FRAMEWORK),squall blacksheep fastapi))
### ========== benchmark GET dataclasses ========== ###
	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=dataclasses \
		FILENAME=/results/userinfo-dataclasses.csv \
		FIXTURE=/fixtures/userinfo.json

	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=dataclasses \
		FILENAME=/results/sprint-dataclasses.csv \
		FIXTURE=/fixtures/sprint.json
endif

## ========== benchmark POST raw ========== ###
	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=raw \
		FILENAME=/results/create-task-raw.csv \
		FIXTURE=/fixtures/create-task.json

ifeq ($(FRAMEWORK),$(filter $(FRAMEWORK),squall blacksheep fastapi))
## ========== benchmark POST dataclasses ========== ###
	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=dataclasses \
		FILENAME=/results/create-task-dataclasses.csv \
		FIXTURE=/fixtures/create-task.json
endif

## ========== benchmark PUT raw ========== ###
	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=raw \
		FILENAME=/results/update-task-raw.csv \
		FIXTURE=/fixtures/update-task.json

ifeq ($(FRAMEWORK),$(filter $(FRAMEWORK),squall blacksheep fastapi))
## ========== benchmark PUT dataclasses ========== ###
	@make benchmark-framework-scenario $(COMMON_WRK) \
		SCENARIO=dataclasses \
		FILENAME=/results/update-task-dataclasses.csv \
		FIXTURE=/fixtures/update-task.json
endif
	@make benchmark-framework-teardown


.PHONY: benchmark
benchmark: # clean
	@make benchmark-f FRAMEWORK=squall
	@make benchmark-f FRAMEWORK=muffin
	@make benchmark-f FRAMEWORK=falcon
	@make benchmark-f FRAMEWORK=blacksheep
	@make benchmark-f FRAMEWORK=emmett
	@make benchmark-f FRAMEWORK=starlette
	@make benchmark-f FRAMEWORK=baize
	@make benchmark-f FRAMEWORK=sanic
	@make benchmark-f FRAMEWORK=aiohttp
	@make benchmark-f FRAMEWORK=fastapi
	@make benchmark-f FRAMEWORK=quart
	@make render

# Run benchmark
%:
	@echo "\nFinished\n"
