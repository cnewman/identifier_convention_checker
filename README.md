# Identifier Name Checker
A tool that scans identifier names and identifies naming problems.

## What's in it
The `fact_extraction_src` file contains C++ code that scans srcML archives and extracts information about identifiers from source code files.

The `identifier_analysis_src` file contains python code that uses the information extracted via srcML to analyze identifier names for naming anti-patterns.

## How to use
You can hook this into a CI using this docker image on [Dockerhub](https://hub.docker.com/repository/docker/sourceslicer/identifier_checker_base)

You can also create your own docker image using the DOCKERFILE that is part of this repository

You can also download/install the tool and run it manually (see below).

## Cloning the repo
Please clone recursive since we are currently using submodules.

`git clone --recursive git@github.com:cnewman/identifier_convention_checker.git`

## Setup and Run
The DOCKERFILE tells you all dependencies, but they'll be copied here for ease:

Some of these are not specific requirements for the checker tool, but for srcML (which the tool relies on).

```
apt-get update && apt-get install --no-install-recommends -y \
    enchant \
    ca-certificates \
    python3-pip \ 
    cmake \
    curl \
    clang \
    make \
    git \
    libxml2-dev \
    libxml2-utils \
    libarchive-dev \
    man \
    dpkg-dev \
    wget \
```

**This is a good time to install srcML, since some of the steps below assume that it is on your machine, and the step above installed srcML's dependencies. Refer to the [srcml](#help-i-dont-know-what-srcml-is) section.**

Now you can install the checker. First, clone it and install everything in the requirements.txt file, then install Spiral.
```
git clone --recursive git@github.com:cnewman/identifier_convention_checker.git
cd identifier_convention_checker 
pip3 install -r requirements.txt
pip3 install git+https://github.com/casics/spiral.git
```

Initialize and update srcSAXEventDispatcher
```
cd identifier_convention_checker/srcSAXEventDispatch 
git submodule init 
git submodule update --remote 
```

Initialize and update srcSAX
```
cd identifier_convention_checker/srcSAXEventDispatch/srcSAX 
git submodule init 
git submodule update --remote
```

Go back to the root directory (identifier_convention_checker), make a build directory, enter the build directory, and build the C++ code

```
mkdir build 
cd build 
cmake .. 
make -j3
```

## How to run the tool

This assumes the incoming file is a file with source code, or a directory.

```
python3 check_identifiers.py [file or directory containing code]
```

The `check_identifiers.py` script runs srcML, then runs the checker. You can run them separately (see check_identifiers.py to understand how), but the easiest way is to just use check_identifiers.py; running them separately is not well-supported. We will document how to run them separately in the future.

## Help, I don't know what srcML is
You can get srcML from here -- https://www.srcml.org/

Loosely speaking (depending on your OS), you need to get the installer and install. Below is how you do it on debian-based systems.

```
wget http://131.123.42.38/lmcrs/v1.0.0/srcml_1.0.0-1_ubuntu20.04.deb
dpkg -i srcml_1.0.0-1_ubuntu20.04.deb
```

# Limitations
Not tested on windows yet :c -- works on Ubuntu, probably most linux distros, and probably mac. There's a good chance it won't compile in windows yet.

It only supports languages that srcML supports: C, C++, Java, C# per https://www.srcml.org/. In addition, It hasn't been tested on anything other than C/C++. That may change depending on the needs of people using the tool. So if you use this and you want to see another language, request it!

# Support
Currently supported by cdnvse [at symbol here] rit (dot symbol) edu
