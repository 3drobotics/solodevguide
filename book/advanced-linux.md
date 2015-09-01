## Yocto Linux

<aside class="danger">
We do not support rebuilding Solo's kernel or compiling binary packages. This documentation is incomplete and will be modified over time.
</aside>

The Linux distribution used is 3DR Poky (based on Yocto Project Reference Distro)
Documentation: http://www.yoctoproject.org/docs/1.8/mega-manual/mega-manual.html

```
# uname -a
Linux 3dr_solo 3.10.17-rt12-1.0.0_ga+g3f15a11 #3 SMP PREEMPT Thu Jun 4 04:07:49 UTC 2015 armv7l GNU/Linux
```

```
# cat /etc/issue
3DR Poky (based on Yocto Project Reference Distro) 1.5.1 \n \l
```

Yocto has a package manager "smart" that can be used to download packages if Solo is connected to the Internet.
