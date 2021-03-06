#!/bin/bash
set -e

project_name=opt-python2
rpm_name=opt-python2
spec_file=/root/rpmbuild/SPECS/${rpm_name}.spec

mkdir -p /root/.config
cat > /root/.config/copr <<EOF
[copr-cli]
login = ${COPR_LOGIN}
username = ${COPR_USERNAME}
token = ${COPR_TOKEN}
copr_url = https://copr.fedoraproject.org
EOF

status=`curl -s -o /dev/null -w "%{http_code}" https://copr.fedoraproject.org/api/coprs/${COPR_USERNAME}/${project_name}/detail/`
if [ $status = "404" ]; then
  copr-cli create --chroot epel-7-x86_64 --description \
'Python2: An interpreted, interactive, object-oriented programming language.
This rpm will be updated with newer upstream verion in the future.
The future version of this rpm maybe incompatible with this version.

This rpm install files to /opt/python2/ and you can use this python alongside the already installed python in CentOS.
' \
--instructions \
"
\`\`\`
sudo curl -sL -o /etc/yum.repos.d/hnakamur-${project_name}.repo https://copr.fedoraproject.org/coprs/hnakamur/${project_name}/repo/epel-7/hnakamur-${project_name}-epel-7.repo\n
\`\`\`

\`\`\`
sudo yum install ${rpm_name}
\`\`\`" \
${project_name}
fi
version=`awk '$1=="Version:" {print $2}' ${spec_file}`
release=$(rpm --eval `awk '$1=="Release:" {print $2}' ${spec_file}`)
srpm_file=/root/rpmbuild/SRPMS/${rpm_name}-${version}-${release}.src.rpm
copr-cli build --nowait ${project_name} ${srpm_file}
