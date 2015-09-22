#!/bin/bash

cd $(dirname $0)/..

gitbook build book
rsync -avz book/_book/. tim@52.6.232.204:/var/www/html
