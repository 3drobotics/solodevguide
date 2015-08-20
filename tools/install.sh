#!/bin/bash

cd $(dirname $0)

# Unpack sshuttle
if [ ! -d sdg/sshuttle ]; then
	git clone https://github.com/apenwarr/sshuttle sdg/sshuttle --depth=1
fi

# update busybox
ssh root@10.1.1.10 "which sv >/dev/null" 
if [ $? -ne 0 ]; then
	wget https://s3.amazonaws.com/solo-packages/3.10.17-rt12/busybox-1.21.1-r1.cortexa9hf_vfp_neon.rpm -P sdg
fi

# rsync
rsync -avz --rsync-path="mkdir -p /opt/sdg && rsync" --progress ./sdg/. root@10.1.1.10:/opt/sdg/.
ssh root@10.1.1.10 "ln -s /opt/sdg/sdg /usr/bin/sdg || true" 2> /dev/null

ssh root@10.1.1.10 "which sv >/dev/null" 
if [ $? -ne 0 ]; then
	scp sdg/busybox-1.21.1-r1.cortexa9hf_vfp_neon.rpm root@10.1.1.10:/tmp/busybox.rpm
	ssh -t root@10.1.1.10 "rpm --replacepkgs -i /tmp/busybox.rpm && echo updated busybox"
fi
