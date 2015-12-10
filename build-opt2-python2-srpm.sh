#!/bin/bash
set -eu
topdir=`rpm --eval '%{_topdir}'`
spec_file=${topdir}/SPECS/opt-python2.spec
version=`awk '$1=="Version:" {print $2}' ${spec_file}`
curl -sL -o ${topdir}/SOURCES/Python-${version}.tar.xz http://www.python.org/ftp/python/${version}/Python-${version}.tar.xz
rpmbuild -bs ${spec_file}
