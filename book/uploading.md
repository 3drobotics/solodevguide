# Installing Files and Code

## Uploading Files

[rsync](https://en.wikipedia.org/wiki/Rsync) is the preferred tool for synchronizing code and files between your desktop and Solo. To copy a file from the local filesystem to Solo:

```sh
rsync -avz local/file/path/. root@10.1.1.10:/solo/path/. 
```

## Installing Packages

Solo is an [rpm](http://www.rpm.org/) based system. These packages can be managed by the [Smart](http://labix.org/smart/) package manager, already installed on your Solo.

[After having installed the *solo-utils* tool](utils.html), from your Solo's shell run:

```sh
solo-utils tunnel-start
```

This tunnels an Internet connection to Solo through your computer. Now we can configure the *Smart* package manager to download packages from a dedicated package repository.

Run this command to add the package repository:

```sh
smart channel --add solo type=rpm-md baseurl=http://solo-packages.s3-website-us-east-1.amazonaws.com/3.10.17-rt12/
```

Now download the package list:

```sh
smart update
```

You can then use `smart search` and `smart install <package>` to install packages. You will see examples used throughout this guide.

These packages are pre-compiled and provided by 3DR for your use. To compile other packages may require rebuilding the Yocto Linux distribution.

<aside class="note">
If you want to restore your package manager state after it's been modified, you can reset it by brute force:

```
yes | smart channel --remove-all
yes | smart channel --add mydb type=rpm-sys name="RPM Database" 
yes | smart channel --add solo type=rpm-md baseurl=http://solo-packages.s3-website-us-east-1.amazonaws.com/3.10.17-rt12/
```
</aside>

## Working with Python

Python 2.7 is used throughout our system and in many of our examples. There are a few ways in which you can deploy Python code to Solo.

<aside class="note">
Some Python libraries are "binary" dependencies. Solo does not ship a compiler (by design) and so cannot install code that requires C extensions. Trial and error is adequate to discovering which packages are usable.
</aside>

<aside class="todo">
Provide ways of compiling code directly for Solo in the "Advanced Topics" section.
</aside>

### Installing using Solo's package manager

Some Python libraries are provided by Solo's internal package manager. For example, `opencv` can be installed via *Smart*, which provides its own Python library. After running:

```sh
smart install python-opencv
```

You can see its Python library is installed:

```sh
$ python -c "import cv2; print cv2.__version__"
2.4.6.1
```

### Bundling Python code

This section shows how to bundle Python code locally on your computer and expand it in a virtual environment ([virtualenv](https://virtualenv.pypa.io/en/latest/)) on Solo. This approach has two benefits:

1. No Internet connection or reliance on package management on Solo is needed.
2. Packages are installed in a virtual environment, so they don't collide with the global Solo namespace.

Create and navigate to a new directory on your host computer. This directory will be populated with your own Python scripts and all their dependencies. The entire directory will then be sent to Solo. 

Start by creating a virtual environment for local use:

```sh
pip install virtualenv
virtualenv env
source ./env/bin/activate
```

We want to configure our environment to not compile any C extensions. We can do this simply in our virtual environment with this command:

```sh
echo 'import sys; import distutils.core; s = distutils.core.setup; distutils.core.setup = (lambda s: (lambda **kwargs: (kwargs.__setitem__("ext_modules", []), s(**kwargs))))(s)' > env/lib/python2.7/site-packages/distutils.pth
```

Now you can install Python packages using `pip install`. When modules require a C extension, they will fail silently, so test your code.

When you're ready to move code over to Solo, you want to create a `requirements.txt` file containing what packages you've installed:

```sh
pip freeze > requirements.txt
```

Next, we want to download these packages on your host computer so they can be moved to Solo along with your code. You can do this using [pip wheel](https://pip.pypa.io/en/latest/reference/pip_wheel.html) to download them into a new folder (`./wheelhouse`). Run this command:

```sh
pip wheel -r ./requirements.txt --build-option="--plat-name=py27"
```

This installs all the dependencies in `requirements.txt` as Python wheel files, which are source code packages.

Next, you can move this entire directory over to Solo using *rsync*:

```sh
rsync -avz --exclude="*.pyc" --exclude="env" ./ solo:/opt/my_python_code
```

SSH into Solo and navigate to the newly made directory (above `/opt/my_python_code`). Finally, run these commands:

```sh
virtualenv env
source ./env/bin/activate
pip install --no-index ./wheelhouse/* -UI
```

This requires no Internet connection. Instead, it installs from all the downloaded dependencies you transferred from your computer. You can now run your Python scripts with any packages you depended on, without having impacted any of Solo's own Python dependencies.


### Installing packages directly with pip

You can install code directly from *pip* on Solo. 

<aside class="note">
This approach will install the package globally. While this is useful for development it is not recommended for distributing code. You may instead consider installing and using [virtualenv](#bundling-python-code) to create isolated environments of packages.
</aside>

Having installed the *solo-utils* utility, run:

```sh
solo-utils install-pip
```

This will install and update *pip* to the latest version. You can then install any packages you like:

```sh
pip install requests
```



