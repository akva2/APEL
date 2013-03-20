#
# spec file for package alberta
#


Name:           alberta
Version:        2.0.1
Release:        0
Summary:        ALBERTA - An adaptive hierarchical finite element toolbox 
License:        GPL-3.0
Group:          Development/Libraries/C and C++
Url:            http://alberta-fem.de
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  lapack-devel libX11-devel mesa-libGL-devel libtool pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:	libalberta2 = %{version}

%description
ALBERTA is an Adaptive multiLevel finite element toolbox using Bisectioning 
refinement and Error control by Residual Techniques for scientific Applications. 
%package -n libalberta2
Summary:        ALBERTA - An adaptive hierarchical finite element toolbox
Group:          System/Libraries

%description -n libalberta2
ALBERTA is an Adaptive multiLevel finite element toolbox using Bisectioning 
refinement and Error control by Residual Techniques for scientific Applications. 
%package devel
Summary:        Development and header files for %{name}
Group:          Development/Libraries/C and C++
Requires:       libalberta2 = %{version}
BuildArch:	noarch

%description devel
This package contains the development and header files for %{name}.

%prep
%setup -q

%build
%configure --disable-shared
make %{?_smp_mflags}

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%clean
rm -rf %{buildroot}

%post -n libalberta2 -p /sbin/ldconfig

%postun -n libalberta2 -p /sbin/ldconfig

%files
%{_datadir}/alberta
%doc AUTHORS README NEWS

%files -n libalberta2
%defattr(-,root,root,-)
%{_libdir}/libalberta_?d.a
%{_libdir}/libalberta_?d.la
%{_libdir}/libalberta_util.a
%{_libdir}/libalberta_util.la

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libexecdir}/libtool.alberta

%files debuginfo
%defattr(-,root,root,-)
%{_libdir}/libalberta_?d_debug.a
%{_libdir}/libalberta_?d_debug.la
%{_libdir}/libalberta_util_debug.a
%{_libdir}/libalberta_util_debug.la
