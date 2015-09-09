#!/bin/bash

SOLO_UTILS_VERSION="1.2.2"

# Unpack sshuttle
echo 'checking for sshuttle....'
ssh root@10.1.1.10 "[[ -d /opt/sshuttle ]]" 2>/dev/null </dev/null
if [[ $? != 0 ]]; then
    echo 'unpacking sshuttle.'
    curl -L https://github.com/apenwarr/sshuttle/archive/master.tar.gz | \
        ssh root@10.1.1.10 "tar -xvzf - -C /tmp && rm -rf /opt/sshuttle && mkdir -p /opt && cp -rf /tmp/sshuttle-master /opt/sshuttle"
fi

# rsync
echo 'checking for solo-utils...'
if [[ $0 == *'install-solo-utils.sh'* ]] && [ -d $(dirname $0)/solo-utils ]; then
    cd $(dirname $0)
    echo 'uploading local solo-utils...'
    rsync -avz --rsync-path="mkdir -p /opt/solo-utils && rsync" --progress ./solo-utils/. root@10.1.1.10:/opt/solo-utils/.
else
    # Unpack solo-utils
    ssh root@10.1.1.10 "[[ -d /opt/solo-utils ]]" 2>/dev/null </dev/null
    if [ $? != 0 ]; then
        echo 'uploading solo-utils from source...'
        curl -L https://bc0a42b65800ec0dd4c9127dde0cd6e98eb70012:x-oauth-basic@github.com/3drobotics/solodevguide/archive/solo-utils-$SOLO_UTILS_VERSION.tar.gz | \
            ssh root@10.1.1.10 "tar -xvzf - -C /tmp && rm -rf /opt/solo-utils && mkdir -p /opt && cp -rf /tmp/solodevguide-solo-utils-* /opt/solo-utils"
    fi
fi
ssh root@10.1.1.10 "ln -s /opt/solo-utils/solo-utils /usr/bin/solo-utils || true" 2>/dev/null </dev/null

# Patch smart to allow --remove-all
# See http://lists.openembedded.org/pipermail/openembedded-core/2014-July/095090.html
# But ather than reinstall smart, just patch the Python code
ssh root@10.1.1.10 "sed -i.bak 's/, \"remove-all\",/, \"remove_all\",/g' /usr/lib/python2.7/site-packages/smart/commands/channel.py" 2>/dev/null </dev/null

# PACKAGE_URL="https://d3isakvpuvm54a.cloudfront.net"
PACKAGE_URL="http://solo-packages.s3-website-us-east-1.amazonaws.com"

# Adds smart repositories.
ssh root@10.1.1.10 <<EOF
smart channel --remove-all -y
smart channel --add rpmsys type=rpm-sys name='RPM Database' -y
smart channel --add all type=rpm-md baseurl=$PACKAGE_URL/3.10.17-rt12/all/ -y
smart channel --add cortexa9hf_vfp_neon type=rpm-md baseurl=$PACKAGE_URL/3.10.17-rt12/cortexa9hf_vfp_neon/ -y
smart channel --add imx6solo_3dr_1080p type=rpm-md baseurl=$PACKAGE_URL/3.10.17-rt12/imx6solo_3dr_1080p/ -y
smart channel --add cortexa9hf_vfp_neon_mx6 type=rpm-md baseurl=$PACKAGE_URL/3.10.17-rt12/cortexa9hf_vfp_neon_mx6/ -y
EOF

install_rpm () {
    name=$1
    file=$2

    echo "checking for $name..."

    ssh -o "StrictHostKeyChecking no" -q root@10.1.1.10 "which $name >/dev/null" </dev/null
    if [ $? -ne 0 ]; then
        curl "$PACKAGE_URL/3.10.17-rt12/cortexa9hf_vfp_neon/$file" | ssh -o "StrictHostKeyChecking no" -q root@10.1.1.10 "cat > /tmp/install.rpm; rpm --replacepkgs -i /tmp/install.rpm && echo installed $file"
    fi
}

# Manual installation of certain pacakges.
echo 'checking rpms...'
install_rpm "sv" "busybox-1.21.1-r1.cortexa9hf_vfp_neon.rpm"

echo 'done. solo-utils is installed and up to date.'
