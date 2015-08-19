#!/bin/bash

cd $(dirname $0)

# Unpack sshuttle
if [ ! -d sdg/sshuttle ]; then
	git clone https://github.com/apenwarr/sshuttle sdg/sshuttle --depth=1
fi

# rsync
rsync -avz --rsync-path="mkdir -p /opt/sdg && rsync" --progress ./sdg/. root@10.1.1.10:/opt/sdg/.
ssh root@10.1.1.10 "ln -s /opt/sdg/sdg /usr/bin/sdg || true" 2> /dev/null
