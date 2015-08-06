# solodevguide

<!--TOC-->
Table of Contents:

* [Linux Distribution](#linux-distribution)
* [SSHing into Solo](#sshing-into-solo)
* [more](#more)
* [documentation license](#documentation-license)

<!--/TOC-->

## Linux Distribution

The linux distribution used is 3DR Poky (based on Yocto Project Reference Distro)
Documentation: http://www.yoctoproject.org/docs/1.8/mega-manual/mega-manual.html
It does have a package manager “Smart”

```
# uname -a
Linux 3dr_solo 3.10.17-rt12-1.0.0_ga+g3f15a11 #3 SMP PREEMPT Thu Jun 4 04:07:49 UTC 2015 armv7l GNU/Linux
```

```
# cat /etc/issue
3DR Poky (based on Yocto Project Reference Distro) 1.5.1 \n \l
```


## SSHing into Solo

To SSH into solo:

```
ssh root@10.1.1.10
```

You'll need the Solo root password. From there, you can use `ssh-copy-id -i ~/.ssh/id_rsa root@10.1.1.10` to have password-less access.

You can optimize this process by adding the following to your .ssh/config file

```
Host solo 10.1.1.10
    Hostname 10.1.1.10
    Port 22
    User root
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    IdentityFile ~/.ssh/id_rsa
```

### Controller

The controller lives at `10.1.1.1`

## more

## documentation license

don't publish this yet!
