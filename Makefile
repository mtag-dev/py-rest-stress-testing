DATE = $(shell date +'%Y-%m-%d')
VIRTUAL_ENV ?= env

$(VIRTUAL_ENV): frameworks/*/requirements.txt
	@[ -d $(VIRTUAL_ENV) ] || python -m venv $(VIRTUAL_ENV)
	find frameworks | grep requirements | xargs -n1 $(VIRTUAL_ENV)/bin/pip install -r
	touch $(VIRTUAL_ENV)

.PHONY:
benchmark-base:
	docker build $(CURDIR) -t benchmark-base

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
			--sysctl net.ipv4.vs.conntrack=0 \
			--sysctl net.ipv4.vs.expire_nodest_conn=1 \
			--sysctl net.ipv4.vs.conn_reuse_mode=0 \
			-v `dirname $(CURDIR)`/squall:/squall \
			-v $(CURDIR)/dummy:/app/dummy \
			-v $(CURDIR)/fixtures:/app/fixtures \
			-v $(CURDIR)/frameworks/schema_dataclasses.py:/app/schema_dataclasses.py \
			-v $(CURDIR)/frameworks/schema_pydantic.py:/app/schema_pydantic.py \
			-p 8080:8080 \
			--name benchmark benchmarks:$(FRAMEWORK)

    ifeq ($(FRAMEWORK),$(filter $(FRAMEWORK),squall squall-dataclass squall-pydantic))
		docker exec benchmark pip install /squall
		@sleep 2
    endif
	@sleep 2
	@echo "\nSetup finished [$(FRAMEWORK)]\n"

.PHONY: benchmark-framework-teardown
benchmark-framework-teardown:
	@echo "\nTeardown framework $(FRAMEWORK)\n--------------------"
	@docker stop benchmark
	@echo "\nTeardown finished [$(FRAMEWORK)]\n"

.PHONY: benchmark-framework-scenario
benchmark-framework-scenario:
	@echo "\nRun fixture $(FIXTURE) [$(FRAMEWORK)]\n"
	@docker run --rm --network bench \
			-e FRAMEWORK=$(FRAMEWORK) -e FILENAME=$(FILENAME) -e FIXTURE=$(FIXTURE) \
			-v $(CURDIR)/fixtures:/fixtures \
			-v $(CURDIR)/results:/results \
			-v $(CURDIR)/wrk:/scripts \
			--sysctl net.core.somaxconn=4096 \
			--sysctl net.ipv4.vs.conntrack=0 \
			--sysctl net.ipv4.vs.expire_nodest_conn=1 \
			--sysctl net.ipv4.vs.conn_reuse_mode=0 \
			czerasz/wrk-json \
			wrk http://benchmark:8080 -d$(DURATION) -t$(THREADS) -c$(CONCURRENT) -s /scripts/process.lua
	@echo "\nFinish [$(FRAMEWORK)]\n"

.PHONY: benchmark-raw
benchmark-raw:
	@make benchmark-framework-setup FRAMEWORK=$(FRAMEWORK)
	@make benchmark-framework-scenario FRAMEWORK=$(FRAMEWORK) \
		FILENAME=/results/userinfo-raw.csv \
		FIXTURE=/fixtures/userinfo.json \
		DURATION=15s \
		CONCURRENT=32 \
		THREADS=4
	@make benchmark-framework-scenario FRAMEWORK=$(FRAMEWORK) \
		FILENAME=/results/sprint-raw.csv \
		FIXTURE=/fixtures/sprint.json \
		DURATION=15s \
		CONCURRENT=32 \
		THREADS=4
	@make benchmark-framework-teardown

.PHONY: benchmark-dataclass
benchmark-dataclass:
	@make benchmark-framework-setup FRAMEWORK=$(FRAMEWORK)
	@make benchmark-framework-scenario FRAMEWORK=$(FRAMEWORK) \
		FILENAME=/results/userinfo-dataclass.csv \
		FIXTURE=/fixtures/userinfo.json \
		DURATION=15s \
		CONCURRENT=32 \
		THREADS=4
	@make benchmark-framework-scenario FRAMEWORK=$(FRAMEWORK) \
		FILENAME=/results/sprint-dataclass.csv \
		FIXTURE=/fixtures/sprint.json \
		DURATION=15s \
		CONCURRENT=32 \
		THREADS=4
	@make benchmark-framework-teardown


.PHONY: benchmark-pydantic
benchmark-pydantic:
	@make benchmark-framework-setup FRAMEWORK=$(FRAMEWORK)
	@make benchmark-framework-scenario FRAMEWORK=$(FRAMEWORK) \
		FILENAME=/results/userinfo-pydantic.csv \
		FIXTURE=/fixtures/userinfo.json \
		DURATION=15s \
		CONCURRENT=32 \
		THREADS=4
	@make benchmark-framework-scenario FRAMEWORK=$(FRAMEWORK) \
		FILENAME=/results/sprint-pydantic.csv \
		FIXTURE=/fixtures/sprint.json \
		DURATION=15s \
		CONCURRENT=32 \
		THREADS=4
	@make benchmark-framework-teardown


.PHONY: benchmark
benchmark: # clean
	@make benchmark-raw FRAMEWORK=aiohttp
	@make benchmark-raw FRAMEWORK=baize
	@make benchmark-raw FRAMEWORK=blacksheep
	@make benchmark-raw FRAMEWORK=emmett
	@make benchmark-raw FRAMEWORK=falcon
	@make benchmark-raw FRAMEWORK=fastapi
	@make benchmark-raw FRAMEWORK=muffin
	@make benchmark-raw FRAMEWORK=quart
	@make benchmark-raw FRAMEWORK=sanic
	@make benchmark-raw FRAMEWORK=starlette
	@make benchmark-raw FRAMEWORK=squall
	@make benchmark-dataclass FRAMEWORK=fastapi-dataclass
	@make benchmark-dataclass FRAMEWORK=blacksheep-dataclass
	@make benchmark-dataclass FRAMEWORK=squall-dataclass
	@make benchmark-pydantic FRAMEWORK=fastapi-pydantic
	@make benchmark-pydantic FRAMEWORK=blacksheep-pydantic
	@make benchmark-pydantic FRAMEWORK=squall-pydantic
	@make render

# Run benchmark
%:
	@echo "\nFinished\n"
