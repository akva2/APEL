#
# spec file for package dune-grid
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


Name:           dune-grid
Version:        2.2.0
Release:        0
Summary:        Grid management module for DUNE
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        http://www.dune-project.org/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  ALUGrid-devel
BuildRequires:  alberta-devel
BuildRequires:  dune-common-devel
BuildRequires:  dune-geometry-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig
BuildRequires:  psurface-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       libdune-grid0 = %{version}

%description
dune-grid defines nonconforming, hierarchically nested, multi-element-type,
parallel grids in arbitrary space dimensions. Graphical output with several
packages is available, e.g. file output to IBM data explorer and VTK (parallel
XML format for unstructured grids). The graphics package Grape has been integrated
in interactive mode. This module also provides some grid implementations and
further grid managers can be added through seprate modules. 

%package -n libdune-grid0
Summary:        Grid management module for DUNE
Group:          System/Libraries

%description -n libdune-grid0
dune-grid defines nonconforming, hierarchically nested, multi-element-type,
parallel grids in arbitrary space dimensions. Graphical output with several
packages is available, e.g. file output to IBM data explorer and VTK (parallel
XML format for unstructured grids). The graphics package Grape has been integrated
in interactive mode. This module also provides some grid implementations and
further grid managers can be added through separate modules. 

%package devel
Summary:        Development and header files for %{name}
Group:          Development/Libraries/C and C++
Requires:       libdune-grid0 = %{version}
BuildArch:	noarch

%description devel
This package contains the development and header files for %{name}.

%prep
%setup -q

%build
%configure --enable-shared --disable-static --without-ug --without-amiramesh
make %{?_smp_mflags}

%install
make install DESTDIR=${RPM_BUILD_ROOT}

find %{buildroot} -name '*.la' -exec rm {} \;

%clean
rm -rf %{buildroot}

%post -n libdune-grid0 -p /sbin/ldconfig

%postun -n libdune-grid0 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_datadir}/doc/dune-grid

%files -n libdune-grid0
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/dune/*
%{_datadir}/aclocal/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/dunecontrol/%{name}
