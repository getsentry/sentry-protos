# Makefile prefers local virtualenv tools when available, and falls
# back to PATH tools when .venv has not been created yet.

# unstable protos are only included in local development and not part of release packages
SENTRY_PROTOS_BUILD_UNSTABLE := 1
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python)
PIP ?= $(if $(wildcard .venv/bin/pip),.venv/bin/pip,pip)
PYTEST ?= $(if $(wildcard .venv/bin/pytest),.venv/bin/pytest,pytest)
SABLEDOCS ?= $(if $(wildcard .venv/bin/sabledocs),.venv/bin/sabledocs,sabledocs)

.PHONY: update-venv
update-venv:
	$(PIP) install -r requirements.txt

# Python client targets
.PHONY: build-py
build-py:
	$(PIP) install -r requirements.txt
	SENTRY_PROTOS_BUILD_UNSTABLE=$(SENTRY_PROTOS_BUILD_UNSTABLE) $(PYTHON) py/generate.py

.PHONY: package-py
package-py:
	make build-py SENTRY_PROTO_BUILD_UNSTABLE=0
	cd py && $(PYTHON) -m build

.PHONY: clean-py
clean-py:
	rm -rf ./py/dist
	rm -rf ./py/sentry_protos
	rm -rf ./py/sentry_protos.egg-info

# Rust client targets
.PHONY: build-rust
build-rust:
	SENTRY_PROTOS_BUILD_UNSTABLE=$(SENTRY_PROTOS_BUILD_UNSTABLE) cargo run -p build_sentry_protos

.PHONY: clean-rust
clean-rust:
	cd rust && cargo clean

repodir := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
.PHONY: update-vendor
update-vendor:
	cd $$(mktemp -d) && \
		git clone -n --depth=1 --filter=tree:0 \
		    https://github.com/protocolbuffers/protobuf && \
		cd protobuf && git sparse-checkout set --no-cone src/google/protobuf && \
		git checkout && rm -rf .git && \
		find . '(' ! -name '*.proto' -a ! -name '*.md' ')' -delete && \
			find . -name '*unittest*' -delete && \
			find . -name 'test_*' -delete && \
	        rm -rf src/google/protobuf/compiler && \
		find . && \
		rm -rf $(repodir)proto/google && \
		mv src/google $(repodir)proto/

.PHONY: build
build: build-py build-rust

# installs protoc if not already installed
.PHONY: ensure-protoc
ensure-protoc:
	@which protoc >/dev/null 2>&1 || ( \
		echo "Installing protoc..." && \
		if [ "$$(uname)" = "Darwin" ]; then \
			brew install protobuf; \
		else \
			echo "Error: Automatic protoc installation not supported on this OS, please install it manually"; \
			exit 1; \
		fi \
	)

.PHONY: docs
docs: ensure-protoc
	$(PIP) install sabledocs
	protoc ./proto/sentry_protos/*/*/*.proto -I ./proto/ -o ./docs/descriptor.pb --include_source_info
	cd docs && $(SABLEDOCS)

.PHONY: test-py
test-py:
	cd py && $(PIP) install -e .
	$(PYTEST) py/tests/
