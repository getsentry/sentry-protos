# seer

Seer protos live under `v2alpha` (`sentry_protos.seer.v2alpha`).

`v1` was published and then removed (it held an unused `IssueSummaryService`), so
new work starts at `v2` rather than reusing `v1` — reusing that version could
collide with the old definitions in existing dependency caches.

See the repo [README](../../../README.md) for schema conventions.
