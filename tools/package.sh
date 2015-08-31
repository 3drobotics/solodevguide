#!/bin/bash

cd $(dirname $0)

VERSION=$(jq -r ".version" sdg/package.json)
git tag -d "solo-utils-$VERSION" || true
git tag -a "solo-utils-$VERSION" -m "solo-utils $VERSION" $(cd $(git rev-parse --show-toplevel) && git subtree split --prefix=tools/sdg)
git push origin "solo-utils-$VERSION" -f
