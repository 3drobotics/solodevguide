#!/bin/bash

cd $(dirname $0)/..

gitbook build book
git add book/_book -f
git commit -am "Publishes to gh-pages."
git push origin `git subtree split --prefix book/_book master`:refs/heads/gh-pages --force
git reset --hard HEAD~1
