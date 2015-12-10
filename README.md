opt-python2-rpm
===============

A Dockerfile to build Python2 rpm for CentOS7 using [Travis CI](https://travis-ci.org/) and [fedora copr](https://copr.fedoraproject.org/).

* This rpm will be updated with newer upstream verion in the future.
* The future version of this rpm maybe incompatible with this version.

This rpm install files to /opt/python2/ and you can use this python alongside the already installed python in CentOS.

# Usage

1. Copy `.envrc.example` to `.envrc`.
2. Go https://copr.fedoraproject.org/api/ and login in and see the values to set.
3. Then modify `.envrc`

Build the docker image to build the opt-python2 srpm file.

```
./build.sh
```

Run the docker image to upload the opt-python2 sprm to copr.

```
source .envrc
./run.sh
```

## License
MIT
