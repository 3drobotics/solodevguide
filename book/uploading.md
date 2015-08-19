# Installing Files and Code

## Uploading Files

`rsync` is the preferred tool for synchronizing code and files between your desktop and Solo. e.g.

```sh
rsync -avz local/file/path/. root@10.1.1.10:/solo/path/. 
```

## Installing Packages

Solo is an `rpm` based system. These packages can be managed by the `smart` package system, already installed on your Solo.

[After having installed the `sdg` tool](utils.html), from your Solo's shell run:

```sh
sdg tunnel-start
```

This tunnels an Internet connection to Solo through your computer. Now we can configure the `smart` package manager to download packages from a dedicated package repository.

Run this command to add the package repository:

```sh
smart channel --add solo https://sdg-packages.s3.amazonaws.com/
```

Now download the package list:

```sh
smart update
```

You can now use `smart search` and `smart install <package>` to install packages. You will see examples used throughout this guide.

These packages are precompiled and provided by 3DR for your use. To compile other packages may require rebuilding the Yocto Linux distribution.

## Working with Python

Python 2.7 is used throughout our system and in many of our examples. There are a few ways in which you can deploy Python code to Solo.

Be aware: some Python libraries are "binary" dependencies. Solo does not ship a compiler (by design) and so cannot install code that requires C extensions. Trial and error is adequate to discovering which packages are usable.

TODO: Provide ways of compiling code directly for Solo in the "Advanced Topics" section.

### Installing packages directly with pip

Using `sdg tunnel`, you can install packages directly from pip.

```sh
python -c "import urllib2; print urllib2.urlopen('https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py').read()" | python
```

### Installing using Solo's package manager

Some Python libraries are provided by Solo's internal package manager. For example, `opencv` can be installed via `smart`, which provides its own Python library. After running:

```
smart install opencv
```

You can see its Python library is installed:

```
python
>>> import cv
>>> cv.__name__
'cv'
```

### Bundling dependencies with virtualenv

If you want to ship specific Python libraries with no chance of your code conflicting with built-in code, you can use virtualenv.
