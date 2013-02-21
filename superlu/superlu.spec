#
# spec file for package superlu (Version 3.0)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           superlu
BuildRequires:  gcc-gfortran tcsh
License:        BSD 3-Clause
Group:          Development/Libraries/C and C++
Summary:        SuperLU matrix solver
Version:        4.3
Release:        141
Source:         superlu_%{version}.tar.gz
Patch0:		00-superlu-make-inc-changes.patch
Url:            http://crd.lbl.gov/~xiaoye/SuperLU/
Prefix:         /usr
BuildRoot:      %{_tmppath}/SuperLU_4.3
Requires:	libsuperlu3 = %{version}

%description
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.

Docu can be found on http://www.netlib.org.

Authors:
--------
    xiaoye@nersc.gov

%package -n libsuperlu3
Summary:        SuperLU matrix solver
Group:          Development/Libraries/C and C++

%description -n libsuperlu3
SuperLU is an algorithm that uses group theory to optimize LU
decomposition of sparse matrices. It's the fastest direct solver for
linear systems that the author is aware of.

Docu can be found on http://www.netlib.org.

Authors:
--------
    xiaoye@nersc.gov

%package devel
Summary:        Development and header files for %{name}
Group:          Development/Libraries/C and C++
Requires:       libsuperlu3 = %{version}
BuildArch:	noarch

%description devel
This package contains the development and header files for %{name}.

%prep
%setup -n SuperLU_%{version}
%patch0 -p1

%build
#cd ../SuperLU
make BUILDROOT=`pwd` #%{?jobs:-j%jobs}
cd lib
gcc -shared -o libsuperlu.so.3 -L. -Wl,--whole-archive -lsuperlu_4.3 -Wl,--no-whole-archive
cd ..

%install
install -d ${RPM_BUILD_ROOT}/%{_docdir}/superlu
mkdir ${RPM_BUILD_ROOT}%{_libdir}
cp -p lib/libsuperlu.so.3 ${RPM_BUILD_ROOT}%{_libdir}/libsuperlu.so.3
pushd ${RPM_BUILD_ROOT}%{_libdir}
ln -sf libsuperlu.so.3 libsuperlu.so
popd
install -d -m 0755 $RPM_BUILD_ROOT/usr/include/superlu
install -m 0644 SRC/*.h $RPM_BUILD_ROOT/usr/include/superlu/
cp -pf README $RPM_BUILD_ROOT/%{_docdir}/superlu/README.SuperLU

%files
%docdir %{_docdir}/superlu
%doc %{_docdir}/superlu

%files -n libsuperlu3
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%dir /usr/include/superlu
/usr/include/superlu/*
%{_libdir}/*.so

%changelog

