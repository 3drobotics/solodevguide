#!/bin/bash

cd $(dirname $0)

# Unpack sshuttle
ssh root@10.1.1.10 "[[ -d /opt/sshuttle ]]"
if [ $? != 0 ]; then
    curl -L https://github.com/apenwarr/sshuttle/archive/master.tar.gz | ssh root@10.1.1.10 "tar -xvzf - -C /tmp && rm -rf /opt/sshuttle && mv /tmp/sshuttle-master /opt/sshuttle"
fi

# rsync
rsync -avz --rsync-path="mkdir -p /opt/sdg && rsync" --progress ./sdg/. root@10.1.1.10:/opt/sdg/.
ssh root@10.1.1.10 "ln -s /opt/sdg/sdg /usr/bin/sdg || true" 2> /dev/null

install_rpm () {
    name=$1
    file=$2

    echo "checking for $name..."

    ssh -o "StrictHostKeyChecking no" -q root@10.1.1.10 "which $name >/dev/null"
    if [ $? -ne 0 ]; then
        curl https://s3.amazonaws.com/solo-packages/3.10.17-rt12/$file | ssh -o "StrictHostKeyChecking no" -q root@10.1.1.10 "cat > /tmp/install.rpm; rpm --replacepkgs -i /tmp/install.rpm && echo installed $file"
    fi
}

install_rpm "sv" "busybox-1.21.1-r1.cortexa9hf_vfp_neon.rpm"
install_rpm "parted" "parted-3.1-r1.cortexa9hf_vfp_neon.rpm"
install_rpm "resize2fs" "libss2-1.42.8-r0.cortexa9hf_vfp_neon.rpm"
install_rpm "resize2fs" "e2fsprogs-1.42.8-r0.cortexa9hf_vfp_neon.rpm"
install_rpm "resize2fs" "e2fsprogs-badblocks-1.42.8-r0.cortexa9hf_vfp_neon.rpm"
install_rpm "mkfs.ext3" "e2fsprogs-mke2fs-1.42.8-r0.cortexa9hf_vfp_neon.rpm"
install_rpm "lsof" "lsof-4.87-r0.cortexa9hf_vfp_neon.rpm"

echo 'done.'
