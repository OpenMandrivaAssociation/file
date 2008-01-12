%define major 1
%define libname %mklibname magic %{major}
%define libname_orig libmagic

Summary:	A utility for determining file types
Name:		file
Version:	4.21
Release:	%mkrel 3
License:	BSD 
Group:		File tools
URL:		ftp://ftp.astron.com/pub/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.bz2
Source1:	magic.mime
# gw fix python linkage
Patch0:		file-4.16-python.patch
Patch3:		file-4.20-selinux.patch
Patch4:		file-4.21-oracle.patch
Patch5:		file-4.20-ppt.patch
Patch6:		file-4.20-ooffice.patch
Patch7:		file-4.20-dump.patch
Patch8:		file-4.20-berkeleydb.patch
Patch9:		file-4.20-xen.patch
Patch10:	file-4.20-clamav.patch
Patch11:	file-4.20-bash.patch
Patch12:	file-4.21-svn.patch
Patch13:	file-4.20-images.patch
Patch14:	file-4.20-apple.patch
Patch15:	file-4.20-magic-misc.patch
Patch16:	file-4.20-audio.patch
Patch17:	file-4.20-add-lzma.patch
Patch18:	file-4.21-lzma-cointainer.patch
Requires:	%{libname} = %{version}
BuildRequires:	zlib-devel
BuildRequires:  python-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{libname}-devel
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

%package -n	%{libname}-static-devel
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{libname}-devel = %{version}
Provides:	%{libname_orig}-static-devel = %{version}-%{release}

%description	-n %{libname}-static-devel
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

%package -n	python-magic
Summary:	Python module to use libmagic
Group:		Development/Python

%description -n	python-magic
Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

This package contains the python binding for libmagic.

%prep
%setup -q
%patch0 -p1
%patch3 -p1 -b .selinux
%patch4 -p1 -b .oracle
%patch5 -p1 -b .ppt
%patch6 -p1 -b .ooffice
%patch7 -p1 -b .dump
%patch8 -p1 -b .berkeley
%patch9 -p1 -b .xen
%patch10 -p1 -b .clamav
%patch11 -p1 -b .bash
%patch12 -p1 -b .svn
%patch13 -p1 -b .images
%patch14 -p1 -b .apple
%patch15 -p1 -b .magic_misc
%patch16 -p1 -b .audio
%patch17 -p1 -b .lzma
%patch18 -p1 -b .lzma_container

#cp %{SOURCE1} magic.mime

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure2_5x \
    --datadir=%{_datadir}/misc

%make

cd python
python setup.py build
cd -

%install
rm -rf %{buildroot}

%makeinstall_std

#install -m0644 magic.mime %{buildroot}%{_datadir}/misc/magic.mime
ln -sf file/magic.mime %{buildroot}%{_datadir}/misc/magic.mime
ln -sf %{name}/magic %{buildroot}%{_datadir}/misc/magic

# install one missing header file
install -m0644 src/file.h %{buildroot}%{_includedir}/

cd python
python setup.py install --prefix=%{buildroot}/%{_prefix}
cd -

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README MAINT LEGAL.NOTICE ChangeLog 
%{_bindir}/*
%{_datadir}/misc/*
%{_mandir}/man1/*
%{_mandir}/man4/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%files -n python-magic
%defattr(-,root,root)
%doc python/README python/example.py 
%{py_platsitedir}/*

