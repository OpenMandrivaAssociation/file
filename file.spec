%define	major	1
%define	libname	%mklibname magic %{major}
%define	devname	%mklibname -d magic
%define	staticname %mklibname -d -s magic

Summary:	A utility for determining file types
Name:		file
Version:	5.12
Release:	2
License:	BSD 
Group:		File tools
URL:		http://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Patch3:		file-4.24-selinux.patch
Patch4:		file-5.04-oracle.patch
Patch7:		file-5.05-dump.patch
Patch8:		file-5.10-berkeleydb.patch
Patch9:		file-4.20-xen.patch
Patch13:	file-5.05-images.patch
Patch14:	file-4.20-apple.patch
Patch24:	file-5.10-sticky-bit.patch
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(python2)

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Shared library for handling magic files

%description -n	%{libname}
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

%package -n	%{devname}
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	magic-devel = %{EVRD}
%define	olddev	%mklibname -d magic 1
%rename		%{olddev}

%description -n	%{devname}
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

%package -n	%{staticname}
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	magic-static-devel = %{EVRD}
%define	oldstat	%mklibname -s -d magic 1
%rename		%{oldstat}

%description -n	%{staticname}
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

%package -n	python-magic
Summary:	Python module to use libmagic
Group:		Development/Python
BuildArch:	noarch
Requires:	%{name} >= %{EVRD}

%description -n	python-magic
Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

This package contains the python binding for libmagic.

%prep
%setup -q
%patch3 -p1 -b .selinux~
%patch4 -p1 -b .oracle~
%patch7 -p1 -b .dump~
%patch8 -p1 -b .berkeley~
%patch9 -p1 -b .xen~
%patch13 -p1 -b .images~
%patch14 -p0 -b .apple~
%patch24 -p1 -b .sticky_bit~
#patch 3
autoreconf -fi

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure2_5x --enable-static
%make

cd python
python setup.py build
cd -

%install
%makeinstall_std
mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libmagic.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libmagic.so.%{major}.*.* %{buildroot}%{_libdir}/libmagic.so

# install one missing header file
install -m644 src/file.h -D %{buildroot}%{_includedir}/file.h

pushd python
python setup.py install --prefix=%{buildroot}%{_prefix}
popd


%files
%doc README MAINT ChangeLog
%{_bindir}/*
%{_datadir}/misc/*
%{_mandir}/man1/*
%{_mandir}/man4/*

%files -n %{libname}
/%{_lib}/libmagic.so.%{major}*

%files -n %{devname}
%{_libdir}/libmagic.so
%{_includedir}/*
%{_mandir}/man3/*

%files -n %{staticname}
%{_libdir}/libmagic.a

%files -n python-magic
%doc python/README python/example.py
%{py_puresitedir}/*

%changelog
* Thu Jan 13 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.12-2
- move library to /%%{_lib} as it's required by /bin/rpm
- use pkgconfig() deps for buildrequires

* Sat Mar 03 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.11-3
+ Revision: 781998
- decrease strength of newly added "C source" patterns (rhbz#772651, P25, Fedora)
- fix detection of ASCII text files with setuid, setgid, or sticky bits (P24,fed)
- add an extra pattern for python matching (P23, from Fedora)
- add application/vnd.ms-tnef mimetype (P22, from Fedora)
- add magic for qemu & vdi images (P21, from Fedora)

* Fri Feb 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.11-2
+ Revision: 780115
- use %%rename macro (fixes obsolete-not-provided)
- use %%{EVRD} macro
- drop excessive provides
- drop explicit library package name dependency
- clean up spec a bit
- increase strength of php matching to take precendence over c-lang, fixing
  misidentification of php scripts as C/C++ (P20)

* Wed Feb 22 2012 Götz Waschk <waschk@mandriva.org> 5.11-1
+ Revision: 779169
- new version

* Fri Feb 10 2012 Oden Eriksson <oeriksson@mandriva.com> 5.10-2
+ Revision: 772464
- remove the libtool *.la file
- various fixes

* Sun Jan 01 2012 Götz Waschk <waschk@mandriva.org> 5.10-1
+ Revision: 748643
- new version
- rediff patch 8

* Mon Sep 26 2011 Götz Waschk <waschk@mandriva.org> 5.09-2
+ Revision: 701244
- rebuild

* Sat Sep 17 2011 Götz Waschk <waschk@mandriva.org> 5.09-1
+ Revision: 700175
- new version

* Fri Aug 05 2011 Götz Waschk <waschk@mandriva.org> 5.08-1
+ Revision: 693271
- new version

* Wed May 11 2011 Funda Wang <fwang@mandriva.org> 5.07-1
+ Revision: 673470
- new version 5.07

* Sat Apr 16 2011 Funda Wang <fwang@mandriva.org> 5.06-1
+ Revision: 653256
- New version 5.06
  use upstream provided lzma and xz detection

* Wed Jan 19 2011 Götz Waschk <waschk@mandriva.org> 5.05-1
+ Revision: 631671
- new version
- drop patches 0,6,12,16
- rediff patches 7,13,17,18
- make python module noarch

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 5.04-2mdv2011.0
+ Revision: 590006
- rebuild for python 2.7

* Sat Jan 23 2010 Funda Wang <fwang@mandriva.org> 5.04-1mdv2010.1
+ Revision: 495189
- rediff oracle patch
- New version 5.04
- rediff ooffice patch

* Sun Oct 11 2009 Frederik Himpe <fhimpe@mandriva.org> 5.03-3mdv2010.0
+ Revision: 456632
- Bump release so that it's higher than the one in 2009.1 updates

  + Götz Waschk <waschk@mandriva.org>
    - fix URL

* Wed May 27 2009 Götz Waschk <waschk@mandriva.org> 5.03-2mdv2010.0
+ Revision: 380178
- fix data dir (blino)

* Thu May 07 2009 Frederik Himpe <fhimpe@mandriva.org> 5.03-1mdv2010.0
+ Revision: 373023
- update to new version 5.03

* Tue May 05 2009 Oden Eriksson <oeriksson@mandriva.com> 5.02-1mdv2010.0
+ Revision: 372197
- 5.02 (fixes CVE-2009-1515)

* Sun May 03 2009 Frederik Himpe <fhimpe@mandriva.org> 5.01-1mdv2010.0
+ Revision: 371017
- Update to new version 5.01
- Rediff lzma patch

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add '~' at end of patch suffixes to avoid possible confusions and ensure
      proper 'ls' coloring

* Wed Feb 04 2009 Götz Waschk <waschk@mandriva.org> 5.00-1mdv2009.1
+ Revision: 337343
- new version
- update patch 19

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - new lzma format has been renamed to xz, update magic accordingly

* Fri Dec 26 2008 Oden Eriksson <oeriksson@mandriva.com> 4.26-2mdv2009.1
+ Revision: 319173
- rediffed some fuzzy pathes
- fix build with -Werror=format-security (P19)

* Mon Sep 01 2008 Frederik Himpe <fhimpe@mandriva.org> 4.26-1mdv2009.0
+ Revision: 278536
- update to new version 4.26

* Wed Jul 16 2008 Götz Waschk <waschk@mandriva.org> 4.25-1mdv2009.0
+ Revision: 236251
- new version
- drop patch 10

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Apr 09 2008 Götz Waschk <waschk@mandriva.org> 4.24-1mdv2009.0
+ Revision: 192489
- new version
- drop source 1
- update patches 3,6,7,8,10,16
- drop patches 5,15
- update file list

* Wed Jan 16 2008 David Walluck <walluck@mandriva.org> 4.23-2mdv2008.1
+ Revision: 153586
- Provides: magic-devel and magic-static-devel

* Sun Jan 13 2008 Götz Waschk <waschk@mandriva.org> 4.23-1mdv2008.1
+ Revision: 151056
- new version
- new devel name
- update patches 7,15,18
- drop patch 11

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - update lzma patch with an improved one from Anders F Bj?\195?\182rklund

* Fri Jun 08 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.21-2mdv2008.0
+ Revision: 37591
- fix path in P18 (I suck)
- add support for future LZMA format (P18)

* Sun Jun 03 2007 Götz Waschk <waschk@mandriva.org> 4.21-1mdv2008.0
+ Revision: 34950
- new version
- rediff patches 4,12
- drop patch 2

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - add lzma support (P17)


* Sat Mar 10 2007 Giuseppe Ghibò <ghibo@mandriva.com> 4.20-1mdv2007.1
+ Revision: 140963
- Release 4.20.
- Removed Patch1 (merged upstream).
- Added Patch2 (merged from ftp://ftp.astron.com/pub/file/)
- Merged Patch3 (selinux), Patch4 (oracle filesystem), Patch5 (powerpoint), Patch6 (openoffice, RH#223297), Patch7 (dump, RH#149868), Patch8 (cracklib, RH#168917), Patch9 (xen), Patch10 (clamav, RH#192406), Patch11 (bash, RH#202185), Patch12 (svn), Patch13 (images), Patch14 (apple) from Fedora, Patch15 (misc/magic) from Fedora/Debian.
- Partially merged Patch16 (audio) from OpenSUSE.

* Tue Jan 09 2007 Götz Waschk <waschk@mandriva.org> 4.19-1mdv2007.1
+ Revision: 106412
- new version

* Thu Dec 14 2006 Nicolas Lẽcureuil <neoclust@mandriva.org> 4.17-6mdv2007.1
+ Revision: 96895
- Rebuild against new python

* Wed Dec 13 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 4.17-5mdv2007.1
+ Revision: 96413
- Recognize Cell SPU objects. Cosmetics for 64-bit PowerPC.

* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 4.17-4mdv2007.1
+ Revision: 74556
- rebuild
- bzip2 cleanup
- bunzip patches and sources
- Import file

* Mon May 15 2006 Stefan van der Eijk <stefan@eijk.nu> 4.17-2mdk
- rebuild for sparc

* Thu Mar 16 2006 Götz Waschk <waschk@mandriva.org> 4.17-1mdk
- drop patch 2

* Thu Mar 16 2006 Götz Waschk <waschk@mandriva.org> 4.17-1mdk
- New release 4.17

* Fri Feb 10 2006 Götz Waschk <waschk@mandriva.org> 4.16-3mdk
- fix python linkage

* Thu Feb 09 2006 Michael Scherer <misc@mandriva.org> 4.16-2mdk
- mkrel
- create python subpackage

* Wed Oct 19 2005 Götz Waschk <waschk@mandriva.org> 4.16-1mdk
- New release 4.16

* Sun Oct 02 2005 Abel Cheung <deaddog@mandriva.org> 4.15-1mdk
- New release 4.15
- Drop upstream patches

* Sat Jul 09 2005 Götz Waschk <waschk@mandriva.org> 4.14-2mdk
- add patch for bug 16740

* Thu Jul 07 2005 Götz Waschk <waschk@mandriva.org> 4.14-1mdk
- New release 4.14

* Thu Jun 02 2005 Abel Cheung <deaddog@mandriva.org> 4.13-2mdk
- Drop Patch1 (already merged)
- Source2: mup support I submitted upstream
- Remove rpmlint warnings

* Mon Feb 14 2005 Götz Waschk <waschk@linux-mandrake.com> 4.13-1mdk
- New release 4.13

* Thu Nov 25 2004 Goetz Waschk <waschk@linux-mandrake.com> 4.12-1mdk
- New release 4.12

* Wed Nov 24 2004 Goetz Waschk <waschk@linux-mandrake.com> 4.11-1mdk
- New release 4.11

* Tue Sep 21 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.10-2mdk
- fix broken mklibname introduced in 4.07-1mdk

* Fri Aug 06 2004 Michael Scherer <misc@mandrake.org> 4.10-1mdk
- New release 4.10

* Mon May 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.09-2mdk
- add one missing header file
- misc spec file fixes

* Sat May 08 2004 Götz Waschk <waschk@linux-mandrake.com> 4.09-1mdk
- add source URL
- New release 4.09

* Sun Apr 04 2004 Götz Waschk <waschk@linux-mandrake.com> 4.08-1mdk
- new version

