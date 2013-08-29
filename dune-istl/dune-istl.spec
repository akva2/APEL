#
# spec file for package dune-istl
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           dune-istl
Version:        2.2.1
Release:        0
Summary:        An iterative solver template library for DUNE
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        http://www.dune-project.org/download/%{version}/%{name}-%{version}.tar.gz
%{?el5:BuildRequires:  boost141-devel}
%{!?el5:BuildRequires: boost-devel}
BuildRequires:  dune-common-devel
%{?el5:BuildRequires: gcc44-c++ gcc44-gfortran}
%{!?el5:BuildRequires: gcc-c++ gcc-gfortran}
BuildRequires:  gmp-devel
BuildRequires:  metis-devel
BuildRequires:  superlu-devel
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       dune-common = %{version}
# Since it is a pure template library..
Requires:	dune-istl-devel = %{version}

%description
dune-istl is the iterative solver template library which provides generic
sparse matrix/vector classes and a variety of solvers based on these classes.
A special feature is the use of templates to exploit the recursive block
structure of finite element matrices at compile time. Available solvers
include Krylov methods, (block-) incomplete decompositions and
aggregation-based algebraic multigrid. 


%package devel
Summary:        Development and header files for DUNE
Group:          Development/Libraries/C and C++
Requires:       dune-common-devel = %{version}
Requires:       gmp-devel
Requires:       metis-devel
Requires:       superlu-devel

%description devel
This package contains the development and header files for DUNE.

%prep
%setup -q

%build
%configure --enable-shared --enable-fieldvector-size-is-method --disable-documentation %{?el5:--with-boost=/usr/include/boost141 --with-boost-libdir=%{_libdir}/boost141} %{?el5:CC=gcc44 CXX=g++44 FC=gfortran44}
make %{?_smp_mflags}

%install
%makeinstall

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_datadir}/doc/dune-istl

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/dunecontrol/%{name}

%changelog

