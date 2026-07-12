# seer

The `sentry_protos.seer.v1` package used to live here. It defined an
`IssueSummaryService` (plus the `SummarizeRequest`/`SummarizeResponse` and
`IssueDetails`/`SentryEventData` messages), added in September 2024.

It was **removed in July 2026** because nothing ever consumed it: neither
[getsentry/seer](https://github.com/getsentry/seer) nor
[getsentry/sentry](https://github.com/getsentry/sentry) imported these
generated bindings. The seer <-> sentry issue-summarization integration was
built over a different transport instead, and the protos sat unused from the
day they were added.

## Adding seer protos again

Do **not** recreate `v1`. Since `v1` was published (to PyPI and crates.io) and
then removed, that version number is burned — reusing it risks colliding with
the old, incompatible definitions in anyone's dependency cache.

Start fresh in `v2`:

```
proto/sentry_protos/seer/v2/<your_service>.proto
```

with `package sentry_protos.seer.v2;`.

See the repo [README](../../../README.md) for the schema conventions and the
note on preferring a new version package over breaking changes.
