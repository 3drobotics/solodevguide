#!/bin/bash

set -e

cd $(dirname $0)

VERSION=$(jq -r ".version" solo-utils/package.json)
git tag -d "solo-utils-$VERSION" || true
git tag -a "solo-utils-$VERSION" -m "solo-utils $VERSION" $(cd $(git rev-parse --show-toplevel) && git subtree split --prefix=tools/solo-utils)
git push origin "solo-utils-$VERSION" -f
