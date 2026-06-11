#!/usr/bin/env bash

set -euo pipefail

if ! command -v devenv >/dev/null 2>&1; then
  echo "devenv is required to bootstrap this worktree." >&2
  echo "Install instructions: https://github.com/getsentry/devenv#install" >&2
  exit 1
fi

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "${repo_root}"

echo "Bootstrapping sentry-protos worktree at ${repo_root}"
devenv sync

if command -v direnv >/dev/null 2>&1 && [ -f .envrc ]; then
  direnv allow "${repo_root}" >/dev/null 2>&1 || true
fi

echo "Worktree setup complete."
