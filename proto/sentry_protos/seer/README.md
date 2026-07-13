# seer

The `sentry_protos.seer.v1` package used to live here (an `IssueSummaryService`
plus its request/response messages). It was removed because nothing consumed it.

## Adding seer protos again

Start in `v2`, not `v1` — `v1` was published and then removed, so reusing that
version could collide with the old definitions in existing dependency caches.

```
proto/sentry_protos/seer/v2/<your_service>.proto   // package sentry_protos.seer.v2;
```

See the repo [README](../../../README.md) for schema conventions.
