# Installing Files and Code

## Uploading Files

*[rsync](https://en.wikipedia.org/wiki/Rsync)* is the preferred tool for synchronizing code and files between your desktop and Solo. To copy a file from the local filesystem to Solo:

<div class="host-code"></div>

```sh
rsync -avz local/file/path/. root@10.1.1.10:/solo/path/. 
```

## Installing Packages

Solo is an [rpm](http://www.rpm.org/) based system. These packages can be managed by the [Smart Package Manager](http://labix.org/smart/) (*Smart*), already installed on your Solo.

These are the requirements for setting up *Smart* to work with our package repositories.

* First, [install the *Solo CLI*](starting-utils.html).
* [Connect to the Internet via `solo wifi`](starting-utils.html#connecting-solo-to-the-internet). This will be needed to download the package lists.
* Run `solo install-smart` to install and download the pacakge repository list.

This command is only needed to be run once. From now on, Solo can download packages when an Internet connection is enabled.

When logged into Solo's terminal, you can explore some of the features of *Smart*:

* `smart install <packagename>` will download and install a package from the repository.
* `smart search <text>` will search for packages matching a given string.

You will see these commands used throughout this guide. These packages are pre-compiled and provided by 3DR for your use. To compile other packages may require [rebuilding via our Yocto Linux distribution](advanced-linux.html).


## Working with Python

Python 2.7 is used throughout our system and in many of our examples. There are a few ways in which you can deploy Python code to Solo.

<aside class="note">
Some Python libraries are "binary" dependencies. Solo does not ship a compiler (by design) and so cannot install code that requires C extensions. Trial and error is adequate to discovering which packages are usable.
</aside>

<aside class="todo">
Provide ways of compiling code directly for Solo in the "Advanced Topics" section.
</aside>


### Installing Python packages using *Smart*

Some Python libraries are provided by Solo's internal package manager. For example, `opencv` can be installed via *Smart*, which provides its own Python library. After running:

```sh
smart install python-opencv
```

You can see its Python library is installed:

```sh
$ python -c "import cv2; print cv2.__version__"
2.4.6.1
```

### Installing packages directly with _pip_

You can install code directly from *pip* on Solo. 

<aside class="note">
Using _pip_ on Solo installs package globally by default. Read the section below about _[virtualenv](#installing-packages-into-a-virtualenv)_ to create isolated environments of packages.
</aside>

Having installed *Solo CLI* on your PC, you can initialize `pip` to work on Solo by running:

<div class="host-code"></div>

```sh
solo install-pip
```

This will install and update *pip* to the latest version. After SSHing into Solo, you can then install packages directly:

```sh
pip install requests
```

We also recommend that you install _git_, as this will be needed to get many of the examples:

```sh
smart install git
```

### Installing packages using the Solo client

The recommended way of working with Python and DroneKit-Python is to use the
[Solo CLI](starting-utils.html#deployingrunning-dronekit-scripts-on-solo) 
to package and run the script in a virtual environment.

<aside class="note">
Solo uses many globally installed packages that may be out of date (in particular, [DroneKit](example-dronekit.html)). Using an isolated environment means that you don't need to update the global versions; potentially disturbing native Solo code.
</aside>

The CLI takes care of packaging all the scripts in a folder:

<div class="host-code"></div>

```
solo script pack
```

The command also packages any dependencies listed in the folder's **requirements.txt** file. A minimal
**requirements.txt** for a dronekit app will look like this:

<div class="any-code"></div>

```
dronekit>=2.0.0
```

You can then transfer the package to Solo, install it, and run it using the command:

<div class="host-code"></div>

```
solo script run yourscriptname.py
```

For more information and examples see [DroneKit:Deploying scripts to Solo](concept-dronekit.html#deploying-scripts-to-solo), [Solo CLI:Deploying and Running DroneKit Scripts on Solo](starting-utils.html#deployingrunning-dronekit-scripts-on-solo) 
and [Example:Hello World](example-helloworld.html).




### Installing packages into a _virtualenv_

The [solo client](#installing-packages-using-the-solo-client) is the easiest way to bundle and run
a Python app into a virtual environment. It is however possible to manually perform the same tasks
using [virtualenv](https://virtualenv.pypa.io/en/latest/).

On Linux and Mac OS X, first install _virtualenv_ on Solo using _pip_:

```sh
pip install virtualenv
```

Next, create (or navigate to) the directory in which your Python code will be run. Run the following command:

```sh
virtualenv env
```

This creates an environment in the local `env/` directory. To "activate" this environment, run this command:

```sh
source ./env/bin/activate
```

You will notice your shell prompt changes to read `(env)root@3dr_solo:`, indicating that you are working in a _virtualenv_.

Now all commands you run from your shell, including launching scripts and installing packages, will only effect this local environment. For example, you can now install a different version of *dronekit* without impacting the global version:

```sh
pip install dronekit
```

The instructions for Windows are similar. The advanced topic [Python bundles](advanced-python.html) shows this process in more detail.


<aside class="note">
The *Smart Package Manager* is written in Python. While you are working in a *virtualenv*, you will notice that *Smart* no longer works! Run `deactivate` at any time to leave the environment.
</aside>
