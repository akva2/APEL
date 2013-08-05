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
Source0:        http://crd-legacy.lbl.gov/~xiaoye/SuperLU/%{name}_%{version}.tar.gz
Patch0:         SuperLU-add-fpic.patch
Patch1:         SuperLU-build-shared-lib3.patch
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
%patch1 -p1
chmod a-x SRC/qselect.c 
cp -p MAKE_INC/make.linux make.inc
sed -i "s|-O3|$RPM_OPT_FLAGS|" make.inc
sed -i "s|\$(SUPERLULIB) ||" make.inc
sed -i "s|\$(HOME)/Codes/%{name}_%{version}|%{_builddir}/%{name}_%{version}|" make.inc

%build
make superlulib

%install
install -d ${RPM_BUILD_ROOT}/%{_docdir}/superlu
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
install -p SRC/libsuperlu.so.%{version} %{buildroot}%{_libdir}
install -p SRC/*.h %{buildroot}%{_includedir}/%{name}
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
cp -Pp SRC/libsuperlu.so %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}
%post -n libsuperlu3 -p /sbin/ldconfig

%postun -n libsuperlu3 -p /sbin/ldconfig

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

