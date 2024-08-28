## 0.1.14

### Various fixes & improvements

- regenerate rust bindings (921c09d2)
- Fix comparison type (#15) by @colin-sentry
- fix comment (#15) by @colin-sentry
- More changes to snuba RPC (#15) by @colin-sentry
- Cleanup generated rust code (d31957f9)

## 0.1.13

### Various fixes & improvements

- regenerate rust bindings (466e747d)
- Refactor the snuba RPC protos (#14) by @colin-sentry
- Simplify (#13) by @markstory
- Switch back to tonic_build (#13) by @markstory
- Add progress output and update Cargo.lock (#13) by @markstory
- Use prost_build instead (#13) by @markstory
- Include version packages based on proto files (#13) by @markstory
- Add codegen steps and buf lint to CI (#12) by @markstory
- Cleanup generated rust code (fefaa088)

## 0.1.12

### Various fixes & improvements

- regenerate rust bindings (1e6ccac9)
- Include Cargo.lock in generated code commit (99ad22e0)
- Fix mistakes (02776dd8)
- Cleanup generated rust code (829ff721)
- Add postrelease script for cleaning up rust packages (8d6ad00b) by @markstory

## 0.1.11

### Various fixes & improvements

- regenerate rust bindings (f6660e65)
- Remove file from package root (df3989be) by @markstory
- Don't use build.rs (c6c97658) by @markstory
- Remove generated rust code from last release attempt (6dcef8c2) by @markstory

## 0.1.10

### Various fixes & improvements

- regenerate rust bindings (91937914)
- Try a different approach to getting a local commit (a7b9806b) by @markstory
- Try commiting rust code before preparing release (74066c39) by @markstory
- Allow generated rust code to be commited (6b9573bb) by @markstory
- craft wants no modified files (3e3c2d7d) by @markstory
- Take a different approach with generating rust code (5b9c41dc) by @markstory
- Expand pre-release script to generate code for rust (bbb642d5) by @markstory

## 0.1.7

### Various fixes & improvements

- Update bump-version to adjust version in Cargo.toml as well. (8ed95317) by @markstory

## 0.1.6

### Various fixes & improvements

- Add metadata that crates.io wants (b61dad90) by @markstory
- Add craft target for crates and toplevel Cargo.toml (ef9dcc19) by @markstory

## 0.1.4

### Various fixes & improvements

- Reorder craft publishing to put github first so I can debug it. (99896f52) by @markstory
- Strip trailing newlines (d675a8d4) by @markstory
- Debugging parse error that shows up in gha but not locally (fe6826ec) by @markstory
- Bump proto version in pyproject as well (#11) by @colin-sentry
- Move things around (#9) by @colin-sentry
- Add request meta (#9) by @colin-sentry
- Add snuba protobuf files (#9) by @colin-sentry
- Protobuf v5 (#10) by @colin-sentry
- Remove intellij files (#8) by @colin-sentry
- Revert changes to rust/lib.rs (#7) by @markstory
- Move js2proto tool into directories that work better with pip install (#7) by @markstory
- Make js2proto more standalone (#7) by @markstory
- Update paths and fix typos (#7) by @markstory
- Document how to do unstable packages (#7) by @markstory
- Move buf configuration file (#7) by @markstory
- Rough in the readme more (#7) by @markstory
- Remove protos from previous location (#7) by @markstory
- Add clean target for rust bindings (#7) by @markstory
- Move protos to the top level (#7) by @markstory
- Clean up python packaging flow (09e49147) by @markstory
- Add license file to generated python code package (d6608241) by @markstory
- Add FSL license (769def88) by @markstory
- add a clean target for python and update dist path (4c8116bd) by @markstory
- Include version number into generated python lib (10c3ce01) by @markstory

_Plus 19 more_

