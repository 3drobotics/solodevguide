#!/bin/bash
VERSION=$(jq -r ".version" sdg/package.json)
git tag -a "solo-utils-$VERSION" -m "solo-utils $VERSION" $(git subtree split --prefix=tools/sdg)
