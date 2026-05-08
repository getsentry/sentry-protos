#!/bin/bash
set -eu

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# shellcheck disable=SC2034
OLD_VERSION="$1"
NEW_VERSION="$2"

# Update VERSION file
echo "$NEW_VERSION" > VERSION

# Update rust/Cargo.toml
perl -pi -e "s/^version = \".*?\"/version = \"$NEW_VERSION\"/" rust/Cargo.toml

# Update Cargo.lock to reflect the new version
cargo generate-lockfile --quiet

echo "New version: $NEW_VERSION"
