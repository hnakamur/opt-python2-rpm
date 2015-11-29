FROM centos:7
MAINTAINER Hiroaki Nakamura <hnakamur@gmail.com>

RUN yum -y install rpmdevtools rpm-build \
 && rpmdev-setuptree

RUN yum -y install epel-release \
 && yum -y install python-pip \
 && pip install copr-cli

ADD opt-python2.spec /root/rpmbuild/SPECS/
ADD *.patch /root/rpmbuild/SOURCES/

RUN version=2.7.10 \
 && curl -sL -o /root/rpmbuild/SOURCES/Python-${version}.tar.xz http://www.python.org/ftp/python/${version}/Python-${version}.tar.xz \
 && rpmbuild -bs /root/rpmbuild/SPECS/opt-python2.spec

ADD copr-build.sh /root/
ENTRYPOINT ["/bin/bash", "/root/copr-build.sh"]
