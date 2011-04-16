%define major 1
%define libname %mklibname magic %{major}
%define develname %mklibname -d magic
%define staticname %mklibname -d -s magic


Summary:	A utility for determining file types
Name:		file
Version:	5.06
Release:	%mkrel 1
License:	BSD 
Group:		File tools
URL:		http://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Patch3:		file-4.24-selinux.patch
Patch4:		file-5.04-oracle.patch
Patch7:		file-5.05-dump.patch
Patch8:		file-4.24-berkeleydb.patch
Patch9:		file-4.20-xen.patch
Patch13:	file-5.05-images.patch
Patch14:	file-4.20-apple.patch
Patch19:	file-5.00-format-strings.patch
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

%package -n	%develname
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libmagic-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:       magic-devel = %{version}-%{release}
Obsoletes:      %mklibname -d magic 1

%description -n	%develname
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

%package -n	%staticname
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%develname = %{version}
Provides:	libmagic-static-devel = %{version}-%{release}
Provides:	magic-static-devel = %{version}-%{release}
Obsoletes:      %mklibname -s -d magic 1

%description	-n %staticname
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

%package -n	python-magic
Summary:	Python module to use libmagic
Group:		Development/Python
BuildArch: noarch
Requires: %name >= %version-%release

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
rm -rf %{buildroot}

%makeinstall_std

# install one missing header file
install -m0644 src/file.h %{buildroot}%{_includedir}/

cd python
python setup.py install --prefix=%{buildroot}/%{_prefix}
cd -

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README MAINT ChangeLog 
%{_bindir}/*
%{_datadir}/misc/*
%{_mandir}/man1/*
%{_mandir}/man4/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3/*

%files -n %staticname
%defattr(-,root,root)
%{_libdir}/*.a

%files -n python-magic
%defattr(-,root,root)
%doc python/README python/example.py 
%{py_puresitedir}/*

