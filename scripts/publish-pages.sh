#!/bin/bash

cd $(dirname $0)/..

gitbook build book
aws s3 sync book/_book/ s3://ffc6904fed514b42b88f87926328069c5c8149f4/ --acl public-read
