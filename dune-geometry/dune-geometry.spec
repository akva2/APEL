#
# spec file for package dune-geometry
#

Name:           dune-geometry
Version:        2.5.1
Release:        0
Summary:        Everything related to the DUNE reference elements
License:        GPL-2.0
Group:          Development/Libraries/C and C++
Url:            http://www.dune-project.org/
Source0:        http://www.dune-project.org/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  dune-common-devel
BuildRequires: gcc-c++ gcc-gfortran
BuildRequires:  gmp-devel
BuildRequires:  pkgconfig devtoolset-6-toolchain
%{?el6:BuildRequires:  cmake3 boost148-devel}
%{?!el6:BuildRequires: cmake boost-devel}
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
mkdir %{_target_platform}
pushd %{_target_platform}
scl enable devtoolset-6 bash
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" %{?el6:cmake3} %{?!el6:cmake} .. -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-6/root/usr/bin/g++ -DCMAKE_C_COMPILER=/opt/rh/devtoolset-6/root/usr/bin/gcc -DCMAKE_Fortran_COMPILER=/opt/rh/devtoolset-6/root/usr/bin/gfortran %{?el6:-DBOOST_LIBRARYDIR=%{_libdir}/boost148 -DBOOST_INCLUDEDIR=%{_includedir}/boost148} -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=1
popd
make -C %{_target_platform} %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%clean
rm -rf %{buildroot}

%post -n libdune-geometry0 -p /sbin/ldconfig

%postun -n libdune-geometry0 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README.md
%{_datadir}/doc/dune-geometry

%files -n libdune-geometry0
%defattr(-,root,root,-)
%{_libdir}/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/%{name}
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*.pc
%{_prefix}/lib/dunecontrol/%{name}
