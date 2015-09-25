## Yocto Linux

<aside class="caution">
This guide does not yet support rebuilding Solo's kernel or compiling binary packages.
</aside>

<aside class="todo">
This section for building binary packages or rebuild Solo's kernel is very incomplete. We are working on rolling out mechanisms for doing so in the coming months. If you are a corporate entity and require this, in the short term, please reach out to 3DR about partnering with our dev team.
</aside>

The Linux distribution used is 3DR Poky (based on [Yocto Project Reference Distro](http://www.yoctoproject.org/docs/1.8/mega-manual/mega-manual.html))

```
# uname -a
Linux 3dr_solo 3.10.17-rt12-1.0.0_ga+g3f15a11 #3 SMP PREEMPT Thu Jun 4 04:07:49 UTC 2015 armv7l GNU/Linux
```

```
# cat /etc/issue
3DR Poky (based on Yocto Project Reference Distro) 1.5.1 \n \l
```

Yocto has a package manager [Smart](https://labix.org/smart) that can be used to download packages if Solo is connected to the Internet.
