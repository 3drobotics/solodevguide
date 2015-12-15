#!/bin/bash

cd $(dirname $0)/..

gitbook build book
ssh-keyscan -t rsa 52.6.232.204 >> ~/.ssh/known_hosts
chmod 600 ~/.ssh/known_hosts
rsync -avz book/_book/. tim@52.6.232.204:/var/www/html
