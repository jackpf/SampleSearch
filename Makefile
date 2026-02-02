PROTO_DIR := proto
PROTO_OUT := src/gen

.PHONY: build-proto
build-proto:
	mkdir -p $(PROTO_OUT)
	protoc \
		-I$(PROTO_DIR) \
		--python_out=$(PROTO_OUT) \
		--pyi_out=$(PROTO_OUT) \
		$(PROTO_DIR)/*.proto

.PHONY: fmt
fmt:
	ruff format src
	ruff check --fix src

.PHONY: lint
lint:
	ruff check src
	mypy src

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run:
	PYTHONPATH=src python -m sample_search.main

