# Uploading Files and Code

`rsync` is your tool.

## Uploading Python Code

Python 2.7 is used throughout our system and in many of our examples. There are a few ways in which you can deploy Python code to Solo.

Be aware: some Python libraries are "binary" dependencies. Solo does not ship a compiler (by design) and so cannot install code that requires C extensions. Trial and error is adequate to discovering which packages are usable.

TODO: Provide ways of compiling code directly for Solo in the "Advanced Topics" section.

### Installing packages directly with pip

Using `sdg tunnel`, you can install packages directly from pip.

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
