# Makefile assumes that direnv is active, or that pip/python on PATH
# is what you want to use.

.PHONY: update-venv
update-venv:
	pip install -r requirements.txt

# Python client targets
.PHONY: build-py
build-py:
	pip install -r requirements.txt
	python py/generate.py

.PHONY: package-py
package-py: build-py
	cd py && python -m build

.PHONY: clean-py
clean-py:
	rm -rf ./py/dist
	rm -rf ./py/sentry_protos
	rm -rf ./py/sentry_protos.egg-info

# Rust client targets
.PHONY: build-rust
build-rust:
	cd rust && cargo build

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
