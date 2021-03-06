# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_with bootstrap
# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_with gui

Name:           cmake28
Version:        2.8.8
Release:        4%{?dist}
Summary:        Cross-platform make system

Group:          Development/Tools

# Most sources are BSD. Source/CursesDialog/form/ a bunch is MIT.
# Source/kwsys/MD5.c is bundled(md5-deutsch) and zlib licensed. Some
# GPL-licensed bison-generated files, these all include an exception
# granting redistribution under terms of your choice
License:        BSD and MIT and zlib
URL:            http://www.cmake.org
Source0:        http://www.cmake.org/files/v2.8/cmake-%{version}.tar.gz
# Patch to find DCMTK in Fedora (bug #720140)
Patch0:         cmake-dcmtk.patch
# (modified) Upstream patch to fix setting PKG_CONFIG_FOUND (bug #812188)
Patch1:         cmake-pkgconfig.patch
# This patch renames the executables with a "28" suffix
Patch2:         cmake28.patch
Patch3:         cmake-macros.patch

# Source/kwsys/MD5.c
# see https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(md5-deutsch)

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} > 5
BuildRequires: gcc-gfortran gcc-c++
%else
BuildRequires: gcc44-gfortran gcc44-c++
%endif
BuildRequires:  ncurses-devel, libX11-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  libarchive-devel
BuildRequires:  zlib-devel
%if %{without bootstrap}
#BuildRequires: xmlrpc-c-devel
%endif
%if %{with gui}
%if 0%{?rhel} > 5
BuildRequires: qt4-devel, desktop-file-utils
%else
BuildRequires: qt46-devel, desktop-file-utils
%endif
%define qt_gui --qt-gui
%endif
Requires:       rpm


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.


%package        gui
Summary:        Qt GUI for %{name}
Group:          Development/Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    gui
The %{name}-gui package contains the Qt based GUI for CMake.


%prep
%setup -q -n cmake-%{version}
%patch0 -p1 -b .dcmtk
%patch1 -p1 -b .pkgconfig
%patch2 -p1 -b .cmake28
%patch3 -p1


%build
%if 0%{?rhel} < 6
export PATH=%{_libdir}/qt46/bin:$PATH
export CC=gcc44
export CXX=g++44
%endif
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
mkdir build
pushd build
../bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
             --docdir=/share/doc/%{name}-%{version} --mandir=/share/man \
             --%{?with_bootstrap:no-}system-libs \
             --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
             %{?qt_gui}
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
popd
cp -a Example $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/cmake28
install -m 0644 Docs/cmake-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/cmake28/cmake28-mode.el
# RPM macros
install -p -m0644 -D macros.cmake28 $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.cmake28
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.cmake28
touch -r macros.cmake28 $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.cmake28
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}

%if %{with gui}
# Desktop file
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/CMake28.desktop
%endif


%check
unset DISPLAY
pushd build
#ModuleNotices fails for some unknown reason, and we don't care
#CMake.HTML currently requires internet access
#CTestTestUpload requires internet access
# Currently broken - disable for now
#bin/ctest28 -V -E ModuleNotices -E CMake.HTML -E CTestTestUpload %{?_smp_mflags}
popd


%clean
rm -rf $RPM_BUILD_ROOT


%if %{with gui}
%post gui
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun gui
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
%endif


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/macros.cmake28
%{_docdir}/%{name}-%{version}/
%if %{with gui}
%exclude %{_docdir}/%{name}-%{version}/cmake28-gui.*
%endif
%{_bindir}/ccmake28
%{_bindir}/cmake28
%{_bindir}/cpack28
%{_bindir}/ctest28
%{_datadir}/aclocal/cmake28.m4
%{_datadir}/%{name}/
%{_mandir}/man1/*
%if %{with gui}
%exclude %{_mandir}/man1/cmake28-gui.1.gz
%endif
%{_datadir}/emacs/site-lisp/cmake28
%{_libdir}/%{name}/

%if %{with gui}
%files gui
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/cmake28-gui.*
%{_bindir}/cmake28-gui
%{_datadir}/applications/CMake28.desktop
%{_datadir}/mime/packages/cmake28cache.xml
%{_datadir}/pixmaps/CMake28Setup32.png
%{_mandir}/man1/cmake28-gui.1.gz
%endif


%changelog
* Thu May 10 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 2.8.8-4
- Further correction to the License tag
- Add Provides: bundled(md5-deutsch)

* Wed May  9 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 2.8.8-3
- Corrected spec file License tag

* Tue May  8 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 2.8.8-2
- Initial package, based on the cmake package
- Some fixes to macros.cmake28
- White space fixes to spec file
- Make -gui require arch specific main package

* Thu Apr 19 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.8-1
- Update to 2.8.8 final

* Sat Apr 14 2012 Rex Dieter <rdieter@fedoraproject.org> 2.8.8-0.4.rc2
- adjust pkgconfig patch (#812188)

* Fri Apr 13 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.8-0.3.rc2
- Add upstream patch to set PKG_CONFIG_FOUND (bug #812188)

* Mon Apr 9 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.8-0.2.rc2
- Update to 2.8.8 RC 2

* Fri Mar 23 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.8-0.1.rc1
- Update to 2.8.8 RC 1

* Tue Feb 21 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-6
- Just strip CMAKE_INSTALL_LIBDIR from %%cmake macro

* Tue Feb 21 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-5
- Strip CMAKE_INSTALL_LIBDIR and others from %%cmake macro (bug 795542)

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 2.8.7-4
- Rebuilt for new libarchive

* Wed Jan 17 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.8.7-3
- Rebuild for libarchive

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 1 2012 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-1
- Update to 2.8.7 final

* Tue Dec 27 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-0.2.rc2
- Update to 2.8.7 RC 2

* Tue Dec 13 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.7-0.1.rc1
- Update to 2.8.7 RC 1

* Tue Nov 15 2011 Daniel Drake <dsd@laptop.org> - 2.8.6-2
- Rebuild for libarchive.so.11

* Wed Oct 5 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.6-1
- Update to 2.8.6 final

* Thu Sep 22 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.6-0.5.rc4
- Update to 2.8.6 RC 4

* Tue Sep 13 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.6-0.4.rc3
- Update to 2.8.6 RC 3

* Sun Sep 11 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.8.6-0.3.rc2
- Sync FFLAGS and LDFLAGS in the %%cmake macro with redhat-rpm-config.

* Tue Sep 6 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.6-0.2.rc2
- Update to 2.8.6 RC 2
- Drop aclocal patch

* Mon Aug 29 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.6-0.1.rc1
- Update to 2.8.6 RC 1
- Update dcmtk patch
- Add upstream patch to fix aclocal install location

* Thu Jul 28 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-3
- Updated patch to find dcmtk in Fedora (Bug #720140)

* Fri Jul 22 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-2
- Add patch to find dcmtk in Fedora (Bug #720140)

* Fri Jul 22 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-1
- Update to 2.8.5 final
- Drop issue 12307 patch

* Thu Jul 21 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-0.3.rc3
- Update to 2.8.5 RC 3
- Drop upstreamed swig patch
- Apply upstream fix for issue 12307 (bug #723652)

* Mon Jun 20 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-0.2.rc2
- Update to 2.8.5 RC 2
- Add patch from upstream to fix FindSWIG

* Tue May 31 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.5-0.1.rc1
- Update to 2.8.5 RC 1
- Disable CTestTestUpload test, needs internet access

* Thu Feb 17 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.4-1
- Update to 2.8.4 final

* Wed Feb 2 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.4-0.2.rc2
- Update to 2.8.4 RC 2

* Tue Jan 18 2011 Orion Poplawski <orion@cora.nwra.com> - 2.8.4-0.1.rc1
- Update to 2.8.4 RC 1
- Drop qt4 patch

* Thu Dec 16 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.3-2
- Add patch from upstream git to fix bug 652886 (qt3/qt4 detection)

* Thu Nov 4 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.3-1
- Update to 2.8.3 final

* Mon Nov 1 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.3-0.3.rc4
- Update to 2.8.3 RC 4
- Drop python 2.7 patch fixed upstream
- No need to fixup source file permissions anymore

* Fri Oct 22 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.3-0.2.rc3
- Update to 2.8.3 RC 3

* Thu Sep 16 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.3-0.1.rc1
- Update to 2.8.3 RC 1
- Add BR bzip2-devel and libarchive-devel

* Fri Jul 23 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.8.2-2
- add support for Python 2.7 to FindPythonLibs.cmake (Orcan Ogetbil)

* Tue Jul 6 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-1
- Update to 2.8.2 final

* Thu Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-0.3.rc4
- Update to 2.8.2 RC 4

* Wed Jun 23 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-0.2.rc3
- Update to 2.8.2 RC 3

* Mon Jun 21 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.2-0.1.rc2
- Update to 2.8.2 RC 2

* Thu Jun 3 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-5
- Upstream published a newer 2.8.1 tar ball

* Wed Jun 2 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-4
- Add BR gcc-gfortran so Fortran support is built

* Wed Apr 21 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-3
- Disable ModuleNotices test, re-enable parallel ctest

* Tue Mar 30 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-2
- Disable parallel ctest checks for now

* Tue Mar 23 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-1
- Update to 2.8.1 final

* Tue Mar 23 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.8.1-0.3.rc5
- Own /usr/lib(64)/cmake/

* Fri Mar 12 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-0.2.rc5
- Update to 2.8.1 RC 5

* Fri Feb 19 2010 Orion Poplawski <orion@cora.nwra.com> - 2.8.1-0.1.rc3
- Update to 2.8.1 RC 3

* Thu Jan 14 2010 Rex Dieter <rdieter@fedorproject.org> - 2.8.0-2
- macros.cmake: drop -DCMAKE_SKIP_RPATH:BOOL=ON from %%cmake

* Wed Nov 18 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-1
- Update to 2.8.0 final

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.8.0-0.8.rc7
- rebuild (for qt-4.6.0-rc1)

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.7.rc7
- Update to 2.8.0 RC 7

* Tue Nov 10 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.7.rc6
- Update to 2.8.0 RC 6

* Wed Nov 4 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.6.rc5
- Update to 2.8.0 RC 5
- Drop patches fixed upstream

* Fri Oct 30 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.5.rc4
- Update to 2.8.0 RC 4
- Add FindJNI patch
- Add test patch from cvs to fix Fedora build test build error

* Tue Oct 13 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.4.rc3
- Update to 2.8.0 RC 3
- Drop vtk64 patch fixed upstream

* Fri Oct 9 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.3.rc2
- Do out of tree build, needed for ExternalProject test

* Thu Oct 8 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.2.rc2
- Update to 2.8.0 RC 2
- Use parallel ctest in %%check

* Tue Sep 29 2009 Orion Poplawski <orion@cora.nwra.com> - 2.8.0-0.1.rc1
- Update to 2.8.0 RC 1

* Thu Sep 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.6.4-4
- macro.cmake: prefixes cmake with the package being builts bindir (#523878)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 3 2009 Orion Poplawski <orion@cora.nwra.com> - 2.6.4-2
- Add patch to find VTK on 64-bit machines (bug #503945)

* Wed Apr 29 2009 Orion Poplawski <orion@cora.nwra.com> - 2.6.4-1
- Update to 2.6.4
- Drop patch for bug #475876 fixed upstream

* Mon Mar 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.6.3-3
- macros.cmake: +%%_cmake_version

* Mon Mar 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.6.3-2
- Fix crash during kdepimlibs build (#475876)

* Mon Feb 23 2009 Orion Poplawski <orion@cora.nwra.com> - 2.6.3-1
- Update to 2.6.3 final

* Tue Feb 17 2009 Orion Poplawski <orion@cora.nwra.com> - 2.6.3-0.4.rc13
- Update to 2.6.3-RC-13

* Tue Jan 13 2009 Orion Poplawski <orion@cora.nwra.com> - 2.6.3-0.3.rc8
- Update to 2.6.3-RC-8

* Sun Jan 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.6.3-0.2.rc5
- macros.cmake: add -DCMAKE_SKIP_RPATH:BOOL=ON
- fix Release tag

* Wed Dec 10 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.3-0.rc5.1
- Update to 2.6.3-RC-5

* Tue Dec 2 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.6.2-3
- Add -DCMAKE_VERBOSE_MAKEFILE=ON to %%cmake (#474053)
- preserve timestamp of macros.cmake
- cosmetics

* Tue Oct 21 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-2
- Allow conditional build of gui

* Mon Sep 29 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-1
- Update to 2.6.2

* Mon Sep 8 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-0.rc3.1
- Update to 2.6.2-RC-2
- Drop parens patch fixed upstream

* Tue Sep 2 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-3
- Drop jni patch, applied upstream.

* Tue Aug 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.6.1-2
- attempt to patch logic error, crasher

* Tue Aug 5 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-1
- Update to 2.6.1

* Mon Jul 14 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-0.rc8.1
- Update to 2.6.1-RC-8
- Drop xmlrpc patch fixed upstream

* Tue May 6 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-1
- Update to 2.6.0

* Mon May 5 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc10.1
- Update to 2.6.0-RC-10

* Thu Apr 24 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc9.1
- Update to 2.6.0-RC-9

* Fri Apr 11 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc8.1
- Update to 2.6.0-RC-8

* Thu Apr 3 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc6.1
- Update to 2.6.0-RC-6

* Fri Mar 28 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc5.1
- Update to 2.6.0-RC-5
- Add gui sub-package for Qt frontend

* Fri Mar 7 2008 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-3
- Add macro for bootstrapping new release/architecture
- Add %%check section

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.8-2
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-1
- Update to 2.4.8

* Wed Jan 16 2008 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-0.rc12
- Update to 2.4.8 RC-12

* Fri Dec 14 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-0.rc4
- Update to 2.4.8 RC-4

* Mon Nov 12 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-4
- No longer set CMAKE_SKIP_RPATH

* Tue Aug 28 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-3
- Rebuild for new expat

* Wed Aug 22 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-2
- Rebuild for BuildID

* Mon Jul 23 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-1
- Update to 2.4.7

* Fri Jun 29 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-0.rc11
- Update to 2.4.7 RC-11

* Wed Jun 27 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-4
- Update macros.cmake to add CMAKE_INSTALL_LIBDIR, INCLUDE_INSTALL_DIR,
  LIB_INSTALL_DIR, SYSCONF_INSTALL_DIR, and SHARE_INSTALL_PREFIX

* Mon Apr 16 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-3
- Apply patch from upstream CVS to fix .so install permissions (bug #235673)

* Fri Apr 06 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-2
- Add rpm macros

* Thu Jan 11 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-1
- Update to 2.4.6

* Mon Dec 18 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.5-2
- Use system libraries (bootstrap --system-libs)

* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.5-1
- Update to 2.4.5

* Tue Nov 21 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.4-1
- Update to 2.4.4

* Tue Oct 31 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-4
- Add /usr/lib/jvm/java to FindJNI search paths

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-3
- Rebuild for FC6

* Wed Aug  2 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-2
- vim 7.0 now ships cmake files, so don't ship ours (bug #201018)
- Add patch to Linux.cmake for Fortran soname support for plplot

* Tue Aug  1 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-1
- Update to 2.4.3

* Mon Jul 31 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.2-3
- Update for vim 7.0

* Tue Jul 11 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.2-2
- Patch FindRuby and FindSWIG to work on Fedora (bug #198103)

* Fri Jun 30 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.2-1
- Update to 2.4.2

* Thu Apr  6 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-4
- Update for vim 7.0c

* Tue Mar 28 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-3
- No subpackages, just own the emacs and vim dirs.

* Tue Mar 21 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-2
- Add emacs and vim support
- Include Example in docs

* Wed Mar  8 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-1
- Fedora Extras version
