#
# spec file for package dune-geometry
#

Name:           dune-geometry
Version:        2.2.1
Release:        0
Summary:        Everything related to the DUNE reference elements
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        http://www.dune-project.org/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  dune-common-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  gmp-devel
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       dune-common = %{version}
Requires:       libdune-geometry0 = %{version}

%description
dune-geometry includes everything related to the DUNE reference elements.
This includes the reference elements themselves, mappings on the reference
elements (geometries), and quadratures. 

%package -n libdune-geometry0
Summary:        Everything related to the DUNE reference elements
Group:          System/Libraries

%description -n libdune-geometry0
dune-geometry includes everything related to the DUNE reference elements.
This includes the reference elements themselves, mappings on the reference
elements (geometries), and quadratures. 

%package devel
Summary:        Development and header files for DUNE
Group:          Development/Libraries/C and C++
Requires:       dune-common-devel = %{version}
Requires:       gmp-devel
Requires:       libdune-geometry0 = %{version}

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

%post -n libdune-geometry0 -p /sbin/ldconfig

%postun -n libdune-geometry0 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_datadir}/doc/dune-geometry

%files -n libdune-geometry0
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/dunecontrol/%{name}
