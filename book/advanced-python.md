# Bundling Python

This guide shows how to bundle Python code locally on your computer and expand it in a virtual environment ([virtualenv](starting-installing.html#installing-packages-into-a-virtualenv)) on Solo. This approach has two benefits:

1. No Internet connection or reliance on package management on Solo is needed.
2. Packages are installed in a virtual environment, so they don't collide with the global Solo namespace.

First create and navigate to a new directory on your host computer. This directory will be populated with your own Python scripts and all their dependencies. The entire directory will then be sent to Solo. 

Start by creating a virtual environment on your host computer:

```sh
pip install virtualenv
virtualenv env
source ./env/bin/activate
```

We want to configure our environment to not compile any C extensions. We can do this simply in our virtual environment with this command:

```sh
echo 'import sys; import distutils.core; s = distutils.core.setup; distutils.core.setup = (lambda s: (lambda **kwargs: (kwargs.__setitem__("ext_modules", []), s(**kwargs))))(s)' > env/lib/python2.7/site-packages/distutils.pth
```

Now you can install Python packages using `pip install`. 

<aside class="warning">
When modules require a C extension, they will fail silently. Test your code!
</aside>

When you're ready to move code over to Solo, create a `requirements.txt` file containing what packages you've installed:

```sh
pip freeze > requirements.txt
```

Next, download these packages on your host computer so they can be moved to Solo along with your code. You can do this by using [pip wheel](https://pip.pypa.io/en/latest/reference/pip_wheel.html) to download them into a new folder (`./wheelhouse`). Run this command:

```sh
pip wheel -r ./requirements.txt --build-option="--plat-name=py27"
```

This installs all the dependencies in `requirements.txt` as Python wheel files, which are source code packages.

Next, you can move this entire directory over to Solo using *rsync*:

```sh
rsync -avz --exclude="*.pyc" --exclude="env" ./ solo:/opt/my_python_code
```

SSH into Solo and navigate to the newly made directory (above `/opt/my_python_code`). Make sure you have _pip_ and _virtualenv_ installed:

```
solo-utils install-pip
pip install virtualenv
```

Finally, run these commands in your Solo code directory:

```sh
virtualenv env
source ./env/bin/activate
pip install --no-index ./wheelhouse/* -UI
```

This requires no Internet connection. Instead, it installs from all the downloaded dependencies you transferred from your computer. You can now run your Python scripts with any packages you depended on, without having impacted any of Solo's own Python dependencies.
