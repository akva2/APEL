#
# spec file for package ALUGrid
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


Name:           ALUGrid
Version:        1.52
Release:        0
Summary:        ALUGrid Library provides both hexahedral and tetrahedral grids
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://aam.mathematik.uni-freiburg.de/IAM/Research/alugrid/
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  metis-devel
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:	libalugrid0 = %{version}

%description
The ALUGrid Library provides both hexahedral and tetrahedral grids which can
be locally adapted and when used for parallel computations the decomposition
of the domain can be recomputed.

%package -n libalugrid0
Summary:        ALUGrid Library provides both hexahedral and tetrahedral grids
Group:          System/Libraries

%description -n libalugrid0
The ALUGrid Library provides both hexahedral and tetrahedral grids which can
be locally adapted and when used for parallel computations the decomposition
of the domain can be recomputed.


%package devel
Summary:        Development and header files for %{name}
Group:          Development/Libraries/C and C++
Requires:       libalugrid0 = %{version}
BuildArch:	noarch

%description devel
This package contains the development and header files for %{name}.

%prep
%setup -q

%build
%configure --enable-shared --disable-static --with-metis=%{_prefix}
make %{?_smp_mflags}

%install
%makeinstall

find %{buildroot} -name '*.la' -exec rm {} \;

%clean
rm -rf %{buildroot}

%post -n libalugrid0 -p /sbin/ldconfig

%postun -n libalugrid0 -p /sbin/ldconfig

%files
%doc AUTHORS README TODO

%files -n libalugrid0
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}/alugridversion

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
