#
# spec file for package libpsurface
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


Name:           psurface
Version:        1.3.1
Release:        0
Summary:        A C++ library that handles piecewise linear bijections between surfaces
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://numerik.mi.fu-berlin.de/dune/psurface/index.php
Source0:        http://numerik.mi.fu-berlin.de/dune/psurface/lib%{name}-%{version}.tar.gz
Patch0:		00-libpsurface-old-automake.patch
BuildRequires:  gcc-c++ automake libtool doxygen
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:	libpsurface0 = %{version}

%description
Psurface is a C++ library that handles piecewise linear bijections between
triangulated surfaces. These surfaces can be of arbitrary shape and need
not even be manifolds. 

%package -n libpsurface0
Summary:        A C++ library that handles piecewise linear bijections between surfaces
Group:          System/Libraries

%description -n libpsurface0
Psurface is a C++ library that handles piecewise linear bijections between
triangulated surfaces. These surfaces can be of arbitrary shape and need
not even be manifolds. 

%package devel
Summary:        Development and header files for %{name}
Group:          Development/Libraries/C and C++
Requires:       libpsurface0 = %{version}

%description devel
This package contains the development and header files for %{name}.

%prep
%setup -q -n lib%{name}-%{version}
%patch0 -p1

%build
autoreconf -if
%configure --enable-shared --disable-static
make %{?_smp_mflags}
cd doc
doxygen

%install
%makeinstall
find %{buildroot} -name '*.la' -exec rm {} \;

%clean
rm -rf %{buildroot}

%post -n libpsurface0 -p /sbin/ldconfig

%postun -n libpsurface0 -p /sbin/ldconfig

%files
%doc COPYING
%doc doc/html

%files -n libpsurface0
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
