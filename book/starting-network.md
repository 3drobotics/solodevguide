# Accessing Solo

When Solo and its Controller are booted, the Controller creates a private network between the two devices over WiFi. Any computer or smartphone can connect to this network and access these devices by their IP address.

Solo's internal network has several endpoints:

* `10.1.1.1` &mdash; Controller
* `10.1.1.10` &mdash; Solo
* `10.1.1.100`&ndash;`10.1.1.255` &mdash; Computers or phones on the network

## Using SSH

SSH is the primary mechanism by which you can access Solo's internals. You can SSH into either Solo or the Controller. 

<aside class="note">
We do not recommend modifying the Controller, and all examples in this guide will be focused on modifying Solo.
</aside>

To SSH into Solo, ensure you have an SSH-capable machine that is connected to the Controller's private network. From your terminal, type:

<div class="host-code"></div>

```
ssh root@10.1.1.10
```

This will prompt you for Solo's root password. The default root password on all Solo devices is:

> TjSDBkAu

Your SSH client will then have direct terminal access to Solo.


### Optimizing SSH

If you do not want to be prompted for a password each time you SSH into Solo, you can run `ssh-copy-id` to copy your password to Solo (installed via `sudo apt-get install ssh-copy-id`, `brew install ssh-copy-id`, etc.):

<div class="host-code"></div>

```
ssh-copy-id -i ~/.ssh/id_rsa root@10.1.1.10
```

You can optimize this process further by adding the following to your `~/.ssh/config`:

<div class="host-code"></div>

```
Host solo 10.1.1.10
    Hostname 10.1.1.10
    Port 22
    User root
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
    IdentityFile ~/.ssh/id_rsa
```

From then on, any Solo device can be accessed by this shorthand:

<div class="host-code"></div>

```
ssh solo
```

<aside class="note">
We will be using the explicit address `root@10.1.1.10` throughout this guide.
</aside>
