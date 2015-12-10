FROM centos:7
MAINTAINER Hiroaki Nakamura <hnakamur@gmail.com>

RUN yum -y install rpmdevtools rpm-build \
 && rpmdev-setuptree

RUN yum -y install epel-release \
 && yum -y install python-pip \
 && pip install copr-cli

ADD opt-python2.spec /root/rpmbuild/SPECS/
ADD *.patch /root/rpmbuild/SOURCES/
ADD build-opt2-python2-srpm.sh /root/rpmbuild/

RUN chmod +x /root/rpmbuild/build-opt2-python2-srpm.sh
# NOTE: I had to separate commands in two RUN's here.
# RUN chmod +x /root/rpmbuild/build-opt2-python2-srpm.sh  && /root/rpmbuild/build-opt2-python2-srpm.sh
# causes the following error:
#   /bin/sh: /root/rpmbuild/build-opt2-python2-srpm.sh: /bin/bash: bad interpreter: Text file busy
RUN /root/rpmbuild/build-opt2-python2-srpm.sh

ADD copr-build.sh /root/rpmbuild/
RUN chmod +x /root/rpmbuild/copr-build.sh
CMD ["/root/rpmbuild/copr-build.sh"]
