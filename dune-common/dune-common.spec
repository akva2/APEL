#
# spec file for package dune-common
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

Name:           dune-common
Version:        2.5.1
Release:        0
Summary:        Distributed and Unified Numerics Environment
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        dune-common-2.5.1.tar.gz
BuildRequires:  blas-devel
BuildRequires: gcc-c++ gcc-gfortran
BuildRequires:  lapack-devel
BuildRequires:  pkgconfig devtoolset-6-toolchain
%{?el6:BuildRequires:  cmake3 boost148-devel}
%{?!el6:BuildRequires:  cmake boost-devel}
BuildRequires:  doxygen
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       libdune-common0 = %{version}

%description
DUNE, the Distributed and Unified Numerics Environment is a modular toolbox
for solving partial differential equations (PDEs) with grid-based methods.
It supports the easy implementation of methods like Finite Elements (FE),
Finite Volumes (FV), and also Finite Differences (FD).

%package -n libdune-common0
Summary:        Distributed and Unified Numerics Environment
Group:          System/Libraries

%description -n libdune-common0
DUNE, the Distributed and Unified Numerics Environment is a modular toolbox
for solving partial differential equations (PDEs) with grid-based methods.
It supports the easy implementation of methods like Finite Elements (FE),
Finite Volumes (FV), and also Finite Differences (FD).

%package devel
Summary:        Development and header files for DUNE
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       blas-devel
Requires:       lapack-devel
Requires:       libdune-common0 = %{version}

%description devel
This package contains the development and header files for DUNE.

%prep
%setup -q

%build
mkdir %{_target_platform}
pushd %{_target_platform}
scl enable devtoolset-6 bash
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" %{?el6:cmake3} %{?el7:cmake} .. -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-6/root/usr/bin/g++ -DCMAKE_C_COMPILER=/opt/rh/devtoolset-6/root/usr/bin/gcc -DCMAKE_Fortran_COMPILER=/opt/rh/devtoolset-6/root/usr/bin/gfortran %{?el6:-DBOOST_LIBRARYDIR=%{_libdir}/boost148 -DBOOST_INCLUDEDIR=%{_includedir}/boost148} -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=1
popd
make -C %{_target_platform} %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%clean
rm -rf %{buildroot}

%post -n libdune-common0 -p /sbin/ldconfig

%postun -n libdune-common0 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README.md TODO
%{_bindir}/*
%{_datadir}/doc/dune-common
%{_datadir}/dune-common
%{_datadir}/man
%{_datadir}

%files -n libdune-common0
%defattr(-,root,root,-)
%{_libdir}/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_prefix}/lib/dune*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake
%{_datadir}/dune

%changelog

