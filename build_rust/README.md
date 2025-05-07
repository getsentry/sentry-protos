# Sentry Protos Rust bindings

Rust bindings for sentry-protos. Enables rust applications to consume protobuf
messages using schema defined in sentry-protos.

## Installation

```
cargo add sentry_protos
```

## Generating bindings

Rust bindings are generated with the `rustgenerator` package. Bindings can be generated using

```shell
# In root of the repository
make build-rust

# Or with
cargo run -p rustgenerator
```
