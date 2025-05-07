#! /usr/bin/env bash

PATHS=(
  rust/src
  Cargo.lock
)

[[ $(git diff --name-only $PATHS) ]] || exit 0

git config user.email bot@getsentry.com
git config user.name getsentry-bot
git add $PATHS
git commit -m 'chore: Regenerate Rust bindings'
