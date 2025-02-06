## 0.1.60

### Various fixes & improvements

- feat(eap-api): supports conditional aggregations (#109) by @xurui-c

## 0.1.59

### Various fixes & improvements

- chore: add label to timeseries expression (#108) by @kylemumma

## 0.1.58

### Various fixes & improvements

- fix(eap): deprecate val_null field (#107) by @davidtsuk

## 0.1.57

### Various fixes & improvements

- feat: Add protos required for EndpointTraceItemStats endpoint (#101) by @shruthilayaj
- feat: formulas in timeseries and traceitemtable endpoints (#105) by @kylemumma

## 0.1.56

### Various fixes & improvements

- feat(eap): Add an is_null field for to AttributeValue (#104) by @davidtsuk

## 0.1.55

### Various fixes & improvements

- fix(eap-api): add sample count to DataPoint for time series (#103) by @xurui-c

## 0.1.54

### Various fixes & improvements

- add trace attributes (#102) by @davidtsuk

## 0.1.53

### Various fixes & improvements

- feat(eap-rpc): Add support for uptime check item type (#99) by @phacops
- chore: Update a comment in endpoint_trace_item_table.proto (#98) by @kylemumma

## 0.1.52

### Various fixes & improvements

- ref(taskbroker): Simplify task activation and retry state (#97) by @enochtangg

## 0.1.51

### Various fixes & improvements

- fix(eap-api): remove comment about deprecation (#96) by @xurui-c

## 0.1.50

### Various fixes & improvements

- fix(eap-api): add TYPE_DOUBLE (#95) by @xurui-c

## 0.1.49

### Various fixes & improvements

- chore: Refactor trace_item_name enum into trace_item_type, add log object (#94) by @colin-sentry

## 0.1.48

### Various fixes & improvements

- fix(eap-api): deprecate `TYPE_DOUBLE` in v1-alpha as well (#93) by @xurui-c

## 0.1.47

### Various fixes & improvements

- fix(eap-api): deprecate TYPE_DOUBLE (#92) by @xurui-c

## 0.1.46

### Various fixes & improvements

- fix(eap): Only allow compraison between aggregation and a double in post aggregation filter (#89) by @davidtsuk

## 0.1.45

### Various fixes & improvements

- c (#88) by @xurui-c

## 0.1.44

### Various fixes & improvements

- c (#87) by @xurui-c
- c (#86) by @xurui-c

## 0.1.43

### Various fixes & improvements

- feat(eap): Add a GetTrace endpoint (#80) by @phacops
- c (#85) by @xurui-c

## 0.1.42

### Various fixes & improvements

- c (#84) by @xurui-c
- feat(eap): Add aggregation filter (#81) by @davidtsuk
- feat(eap): Add more span name fields to the trace (#79) by @phacops
- feat: add ignore_case boolean to ComparisonFilter (#83) by @kylemumma
-  bug: cant commit to any branch locally (#82) by @kylemumma
- feat: no local commits to main branch (#77) by @kylemumma

## 0.1.41

### Various fixes & improvements

- feat(eap): Add a GetTraces endpoint (#71) by @phacops
- feat: add docs for TraceItemTable endpoint (#78) by @kylemumma
- feat: improve docs of AttributeValues and Timeseries endpoint (#76) by @kylemumma
- feat: improve documentation of TraceItemAttributeNames endpoint (#74) by @kylemumma
- feat: add ensure-protoc to makefile (#73) by @kylemumma
- chore: Update to buf-action (#72) by @markstory

## 0.1.40

### Various fixes & improvements

- Add default value to virtual column context (#70) by @davidtsuk

## 0.1.39

### Various fixes & improvements

- feat(taskbroker): Improve fetch_next (#69) by @enochtangg

## 0.1.38

### Various fixes & improvements

- add namespace parameter to get/set requests (#68) by @enochtangg
- ref(taskbroker) Add at_most_once flag to task activations (#66) by @evanh
- Use a reliability enum instead of boolean (#65) by @davidtsuk
- Add reliability to timeseries results (#64) by @davidtsuk
- feat: add p75 (#63) by @wmak
- feat(subscriptions): Create subscriptions uses timeseries request (#60) by @shruthilayaj
- feat: Run examples as tests and add tests for taskworker (#62) by @markstory
- feat(tasks): Add protos for the ConsumerService (#61) by @evanh
- feat(taskworker): Add processing deadline and expiration (#59) by @enochtangg
- feat(subscriptions): Adds protobuf for create table subscription endpoint (#58) by @edwardgou-sentry
- feat: TraceItemAttributeNames, add response metadata to Response, add page tokens (#57) by @kylemumma
- Use AttributeKey in TraceItemAttributeValuesRequest (#55) by @volokluev
- Add trace logging support to ResponseMeta (#54) by @nachivrn
- Set taskworker proto to v1 (#53) by @john-z-yang
- Add definitions for taskworker tasks (#52) by @john-z-yang
- Add QueryStats and QueryMetadata to TraceItemTableResponse (#51) by @nachivrn
- try to fix imports (#46) by @evanh
- add orderby, use enum for item name (#46) by @evanh
- add event filter to page token (#46) by @evanh
- add event filter to page token (#46) by @evanh
- Deprecate FUNCTION_AVERAGE (#50) by @volokluev
- fix filters (#46) by @evanh
- comment fixes (#46) by @evanh
- Cleanup (#49) by @markstory

_Plus 43 more_

## 0.1.22

### Various fixes & improvements

- chore(docs) Improve local development setup (#32) by @markstory
- allow building multiple versions (#31) by @volokluev
- Drop even more files (#29) by @corps
- More filtering (#29) by @corps
- Improving vendor by filtering unittest files (#29) by @corps
- Adds seer summary endpoints (#30) by @corps
- Support vendored google protobuf sources. Generated files are distributed with protobuf libraries, so they do not need to be built even if they are referenced. (#29) by @corps
- add value substring (#25) by @volokluev
- save request_common.proto (#25) by @volokluev
- move trace item name to meta, add enum (#25) by @volokluev
- add trace_item_name to payload (#25) by @volokluev
- separate value types in endpoint (#25) by @volokluev
- pluralize virtual column contexts (#24) by @volokluev
- Create CODEOWNERS (a4a5b3fb) by @volokluev
- Revert "chore: add an experimental flag to spansamples endpoint to use subquery" (#22) by @colin-sentry
- Make release instructions more clear (01faca9c) by @volokluev
- release: 0.1.20 (6b40d796) by @getsentry-bot
- chore: add an experimental flag to spansamples endpoint to use subquery (#20) by @colin-sentry

## 0.1.20

- No documented changes.

## 0.1.19

### Various fixes & improvements

- We don't need a post-release script anymore (199e4673)

## 0.1.18

### Various fixes & improvements

- Restore top-level cargo.toml (de9ae122)
- Rename variable (#19) by @markstory
- Remove release commits. (#19) by @markstory
- Update build tooling for rust client to use build.rs (#19) by @markstory
- Remove workspace cargo.toml (#19) by @markstory
- Cleanup generated rust code (08744b64)

## 0.1.16

### Various fixes & improvements

- regenerate rust bindings (df1d3142)
- feat(eap): add a snuba tags list endpoint (#17) by @colin-sentry
- Cleanup generated rust code (af63599f)

## 0.1.15

### Various fixes & improvements

- regenerate rust bindings (258607eb)
- derp (#16) by @colin-sentry
- Cleanup generated rust code (0945af1b)

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

