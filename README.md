  # sentry-protos

Protocol buffers and gRPC schema for cross-process communication. Contains tooling to generate python and rust client bindings.

📗 [Notion documentation](https://www.notion.so/sentry/Protobuf-gRPC-schema-registry-7325ddca05dc49a5b05aa317c5dd1641)

# Defining schemas

Message schemas are defined in the `protos` directory. Messages and services are 
organized by service or product domain and version.

All proto files are required to define a `package` that reflects the filesystem path to the proto file,
and must end in a version specifier. 

## Backwards compatibility

We use `buf lint` to validate that changes to existing schemas are backwards compatible with
previously published schemas. If breaking changes are required it is recommended to create a new version
package instead of trying to ship a potentially breaking change.

## Unstable versions

While features are in development, we occasionally need to break backwards compatibility.
Any proto packages that end in `alpha`, `beta`, or `test` are exempt from breaking change validation.

For example: `sentry_protos.sentry.confabulator.v1test` would not be subject to backwards compatibility.

Unstable protocols are not included in release packages in order to prevent them from being
used in production workloads.

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
pip install -e ../sentry-protos/py --config-settings editable_mode=strict
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

# Releasing

Use the `release` workflow in GitHub actions to create new releases. Each time a release is created, packages will be published for each supported language.

In this repo, click on Actions:

![image](https://github.com/user-attachments/assets/ce9f638e-5f16-4ff7-9457-d92d2738dc06)

Select `release`

![image](https://github.com/user-attachments/assets/c818995b-fcba-4210-b5a0-8524712315a2)

click `Run Workflow` to create a new release, update version according to [semver guidelines](https://semver.org/)

![image](https://github.com/user-attachments/assets/b2abb910-1d22-428a-811b-1e79d6cbb75d)

