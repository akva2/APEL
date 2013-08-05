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
Version:        2.2.0
Release:        0
Summary:        Distributed and Unified Numerics Environment
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        http://www.dune-project.org/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  blas-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  lapack-devel
BuildRequires:  pkgconfig
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
BuildArch:	noarch

%description devel
This package contains the development and header files for DUNE.

%prep
%setup -q

%build
%configure --enable-shared --disable-static
make %{?_smp_mflags}

%install
%makeinstall

find %{buildroot} -name '*.la' -exec rm {} \;

%clean
rm -rf %{buildroot}

%post -n libdune-common0 -p /sbin/ldconfig

%postun -n libdune-common0 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/*
%{_datadir}/dune-common
%{_datadir}/doc/dune-common
%{_libdir}/dunecontrol
%{_libdir}/dunemodules.lib

%files -n libdune-common0
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog

