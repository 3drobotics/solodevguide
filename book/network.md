## Solo's Network

Solo's internal network has several endpoints:

* `10.1.1.10` &mdash; Solo
* `10.1.1.1` &mdash; the Controller

### Using SSH

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
