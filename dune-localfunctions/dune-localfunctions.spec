
# spec file for package dune-localfunctions
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


Name:           dune-localfunctions
Version:        2.3.1
Release:        0
Summary:        An interface and implementation for shape functions defined on the DUNE
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        http://www.dune-project.org/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  dune-common-devel
BuildRequires:  dune-geometry-devel
BuildRequires:  dune-grid-devel boost148-devel
%{?el5:BuildRequires: gcc44-c++ gcc44-gfortran}
%{!?el5:BuildRequires: gcc-c++ gcc-gfortran}
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       dune-common = %{version}
Requires:       dune-geometry = %{version}
%{?el6:Requires:       cmake28}
%{?!el6:Requires:       cmake}

%description
dune-localfunctions provides interface and implementation for shape functions
defined on the DUNE reference elements. In addition to the shape function,
interpolation operators and special keys are provided which can be used to
assemble global function spaces on finite-element localfunctionss.

%package devel
Summary:        Development and header files for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       dune-common-devel = %{version}
Requires:       dune-geometry-devel = %{version}
Requires:       dune-grid-devel = %{version}
BuildArch:      noarch

%description devel
This package contains the development and header files for %{name}.

%prep
%setup -q

%build
mkdir %{_target_platform}
pushd %{_target_platform}
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" %{?el6:cmake28} %{?!el6:cmake} .. -DCMAKE_INSTALL_PREFIX=%{_prefix} %{?el5:-DCMAKE_C_COMPILER=gcc44 -DCMAKE_CXX_COMPILER=g++44 -DCMAKE_Fortran_COMPILER=gfortran44} -DBOOST_LIBRARYDIR=%{_libdir}/boost148 -DBOOST_INCLUDEDIR=/usr/include/boost148 -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=1
popd
make -C %{_target_platform} %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_datadir}/doc/dune-localfunctions

%files devel
%defattr(-,root,root,-)
%{_includedir}/dune/localfunctions
%{_datadir}/aclocal/*
%{_datadir}/dune
%{_datadir}/dune-localfunctions
%{_prefix}/lib/cmake
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/dunecontrol/%{name}
