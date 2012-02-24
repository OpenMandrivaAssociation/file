%define	major	1
%define	libname	%mklibname magic %{major}
%define	devname	%mklibname -d magic
%define	staticname %mklibname -d -s magic

Summary:	A utility for determining file types
Name:		file
Version:	5.11
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
Patch19:	file-5.00-format-strings.patch
Patch20:	file-5.11-increase-strength-of-php-matching-to-take-precendence-over-c-lang.patch
BuildRequires:	zlib-devel
BuildRequires:  python-devel

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
Obsoletes:	%mklibname -d magic 1

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
Obsoletes:	%mklibname -s -d magic 1

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
%patch20 -p1 -b .php~

#patch 3
autoreconf -fi

#cp %{SOURCE1} magic.mime

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure2_5x
%make

cd python
python setup.py build
cd -

%install
%makeinstall_std

# install one missing header file
install -m644 src/file.h -D %{buildroot}%{_includedir}/file.h

cd python
python setup.py install --prefix=%{buildroot}%{_prefix}
cd -

# cleanups
rm -f %{buildroot}%{_libdir}/*.la

%files
%doc README MAINT ChangeLog
%{_bindir}/*
%{_datadir}/misc/*
%{_mandir}/man1/*
%{_mandir}/man4/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%files -n %{staticname}
%{_libdir}/*.a

%files -n python-magic
%doc python/README python/example.py
%{py_puresitedir}/*
