# Physical Units and Quantities (PUQ)

Implementation of physical unit calculations in C++.
The original project written in Python is available in the [scinumtools](https://github.com/vrtulka23/scinumtools) package.

## Example of use

In order to compile PUQ you can use the following setup script.

``` bash
./setup.sh -h         # display help
./setup.sh -b -t      # build and test
sudo ./setup.sh -i    # install `puq` executable into bin directory
...
```

Compiled PUQ executable can be then run directly from a terminal.

``` bash
puq -h                 # display help
puq -i "J/s"           # expression information
puq -c "12*J" "erg"    # conversion of units
puq -c US "yd" SI "au" # conversion between unit systems
...
```

## Homebrew installation on Mac OS

On Apple systems it is possible to install PUQ as a Homebrew package.
So far, PUQ is not included in the homebrew/core repository.
It will be moved there in the future, also with other scinumtools projects.

``` bash
brew tap vrtulka23/scinumtools
brew install vrtulka23/scinumtools/scnt-puq
```
