%global _prefix /opt/python2

# Do not check rpaths
%global __arch_install_post /usr/lib/rpm/check-buildroot

# Do not byte compile with /usr/lib/rpm/brp-python-bytecompile
%global __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:\
    /usr/lib/rpm/redhat/brp-strip %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
    } \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-python-hardlink \
    %{!?__jar_repack:/usr/lib/rpm/redhat/brp-java-repack-jars} \
%{nil}

%global debug_package %{nil}

%global unicode ucs4
%global with_systemtap 0

%global with_gdbm 1

# some arches don't have valgrind so we need to disable its support on them
%ifarch %{arm} %{ix86} x86_64 ppc %{power64} s390x
%global with_valgrind 1
%else
%global with_valgrind 0
%endif

%global pybasever 2.7

Summary: An interpreted, interactive, object-oriented programming language
Name: opt-python2
Version: 2.7.11
Release: 1%{?dist}
License: Python
Group: Development/Languages
Vendor: The Python Software Foundation
Packager: Hiroaki Nakamura https://github.com/hnakamur

Source: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
URL: http://www.python.org/

# Only used when "%{_lib}" == "lib64"
# Fixup various paths throughout the build and in distutils from "lib" to "lib64",
# and add the /usr/lib64/pythonMAJOR.MINOR/site-packages to sitedirs, in front of
# /usr/lib/pythonMAJOR.MINOR/site-packages
# Not upstream
Patch102: python-2.7.10-lib64.patch

# Python 2.7 split out much of the path-handling from distutils/sysconfig.py to
# a new sysconfig.py (in r77704).
# We need to make equivalent changes to that new file to ensure that the stdlib
# and platform-specific code go to /usr/lib64 not /usr/lib, on 64-bit archs:
Patch103: python-2.7-lib64-sysconfig.patch

# 00104 #
# Only used when "%{_lib}" == "lib64"
# Another lib64 fix, for distutils/tests/test_install.py; not upstream:
Patch104: 00104-lib64-fix-for-test_install.patch


# (keep this list alphabetized)

BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: db4-devel
BuildRequires: expat-devel
BuildRequires: findutils
BuildRequires: gcc-c++
%if %{with_gdbm}
BuildRequires: gdbm-devel
%endif
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: libdb-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel

%if 0%{?with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel

%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif

BuildRequires: zlib-devel

# NOTE: Workaround for the "/usr/local/bin/python is needed by opt-python2-2.7.10-1.el7.centos.x86_64" error when installing this rpm
# See http://stackoverflow.com/questions/7423300/python-rpm-i-built-wont-install/7423994#7423994
# AutoReq: no

Provides: %{name}-abi = %{pybasever}
Provides: %{name}(abi) = %{pybasever}

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface.

Note that documentation for Python is provided in the python-docs
package.

This package provides the "python" executable; most of the actual
implementation is within the "python-libs" package.

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%setup -q -n Python-%{version}
%if "%{_lib}" == "lib64"
%patch102 -p1 -b .lib64
%patch103 -p1 -b .lib64-sysconfig
%patch104 -p1
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
# See http://qiita.com/methane/items/bf0b74550bee125cdea4
%configure \
  --prefix=%{_prefix} \
  --enable-ipv6 \
  --enable-shared \
  --enable-unicode=%{unicode} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
%if 0%{?with_systemtap}
  --with-dtrace \
%endif
%if 0%{?with_valgrind}
  --with-valgrind \
%endif
  LDFLAGS="-Wl,-rpath,%{_libdir} -Wl,-rpath,%{_libdir}/python%{pybasever}/lib-dynload" \
  %{nil}

make EXTRA_CFLAGS="$CFLAGS" %{?_smp_mflags}


# ======================================================
# Installing the built code:
# ======================================================

%install
export topdir=$(pwd)
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
LD_LIBRARY_PATH="$topdir" ./python Tools/scripts/pathfix.py -i %{_prefix}/bin/python %{buildroot}
find %{buildroot} -name "*~" |xargs rm -f

# ======================================================
# Running the upstream test suite
# ======================================================

%check
make test

# ======================================================
# Cleaning up
# ======================================================

%clean
rm -fr %{buildroot}

%files
%defattr(-, root, root, -)
/*

# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
* Sun Nov 29 2015 Hiroaki Nakamura <hnakamur@gmail.com> - 2.7.10-1
- Python-2.7.10
