Name: metis
Summary: Serial Graph Partitioning and Fill-reducing Matrix Ordering
Version: 5.0.2
Release: 0
License: BSD-like
Group:   Productivity/Graphics/3D Editors  
URL: http://glaros.dtc.umn.edu/gkhome/metis/metis/overview
Source0: http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/%{name}-%{version}.tar.gz
Patch0: 00-metis-out-of-tree-build.patch
Patch1: 01-metis-set-soversion.patch
Patch2: 02-metis-honor-lib64.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: make gcc gcc-c++ pkgconfig cmake28
Requires:      libmetis0 = %{version}

%description
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%package -n libmetis0
Summary:        Serial Graph Partitioning and Fill-reducing Matrix Ordering
Group:          System/Libraries

%package devel
License:         Free for non-commercial use
Requires:        %name = %version
Requires:	 pkgconfig
Summary:         Metis development files
Group:           Development/Libraries/C and C++

%description -n libmetis0
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%description devel
METIS is a family of programs for partitioning unstructured graphs and hypergraph
and computing fill-reducing orderings of sparse matrices. The underlying algorithms
used by METIS are based on the state-of-the-art multilevel paradigm that has been
shown to produce high quality results and scale to very large problems.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" cmake28 . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DSHARED=1
%__make %{?jobs:-j%{jobs}}

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%post -n libmetis0
/sbin/ldconfig

%postun -n libmetis0
/sbin/ldconfig

%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc Changelog
%doc manual/manual.pdf

%files -n libmetis0
%_bindir/*
%_libdir/libmetis.so.*

%files devel
%defattr(-,root,root)
%_includedir/metis.h
%_libdir/libmetis.so
