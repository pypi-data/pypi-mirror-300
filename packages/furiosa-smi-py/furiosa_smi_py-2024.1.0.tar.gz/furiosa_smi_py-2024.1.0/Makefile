.PHONY: build
build:
	cargo build

.PHONY: install
install:
	maturin develop --locked -r -E test

.PHONY: fmt
fmt:
	cargo fmt --all --check
	cargo machete
	cargo sort --grouped --workspace

.PHONY: clippy
clippy:
	cargo fmt --all --check && cargo -q clippy --all-targets -- -D rust_2018_idioms -D warnings

.PHONY: rust_tools
rust_tools:
	rustup component add clippy rustfmt
	cargo install --force cargo-sort cargo-machete

.PHONY: clean
clean:
	cargo clean

.PHONY: example
example:
	python3 examples/list_devices.py
	python3 examples/show_topology.py
