# sentry-protos

An ongoing experiment / demo with using protos and gRPC and sentry.  Currently holds a few demo
schemas, but is not actively used in production.

https://www.notion.so/sentry/Protobuf-gRPC-schema-registry-7325ddca05dc49a5b05aa317c5dd1641

# Publishing protos

Use the `release` workflow in GitHub actions to create new releases. Each time a release is created, packages will be published for each supported language.

# Unstable protos

While features are in development, we occasionally need to break backwards compatibility.
Any proto packages that end in `alpha`, `beta`, or `test` are exempt from breaking change validation.

For example: `sentry_protos.sentry.confabulator.v1test` would not be subject to backwards compatibility.

# Local development workflow

sentry-protos makes it easy to develop and test protobuf/grpc changes locally before making
pull requests.

You'll need a local clone of this repository to start.

## Python

From the root of `sentry-protos` run:

```shell
make build-py
```

Then in your application install the python bindings with pip.

```shell
# CWD is in your python application
pip install -e ../sentry-protos/py
```

As you make changes to proto files, you will need to regenerate bindings with `make build-py`.

## Rust

From the root of `sentry-protos` run:

```shell
make build-rust
```

Your application's `Cargo.toml` will need the following:

```toml
[dependencies]
sentry_protos = "0.1.0"

[patch.crates-io]
sentry_protos = { path = "../sentry-protos/rust/" }
```

### Rust conventions

Rust code generation applies some naming conventions that you need to keep in mind when consuming generated code.

#### Enums within Messages

Enums that are nested within messages will be hoisted into a namespace matching the snake_case name of the message. For example:

```proto
// Defined in sentry_protos/snuba/v1alpha/trace_item_attribute.proto
message AttributeKey {
  enum Type {
    TYPE_UNSPECIFIED = 0;
    TYPE_BOOLEAN = 1;
  }
}

```

The `Type` enum would be available as `sentry_protos::snuba::v1alpha::attribute_key::Type`. While `AttributeKey` can be imported from `sentry_protos::snuba::v1alpha::AttributeKey`.



