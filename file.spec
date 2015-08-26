%define	major	1
%define	libname	%mklibname magic %{major}
%define	devname	%mklibname -d magic
%define	static	%mklibname -d -s magic

%bcond_with uclibc

Summary:	A utility for determining file types
Name:		file
Version:	5.24
Release:	3
License:	BSD
Group:		File tools
Url:		http://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch3:		file-4.24-selinux.patch
Patch4:		file-5.04-oracle.patch
Patch7:		file-5.05-dump.patch
Patch8:		file-5.10-berkeleydb.patch
Patch9:		file-5.14-xen.patch
Patch13:	file-5.05-images.patch
Patch14:	file-4.20-apple.patch
Patch26:	file-rpm-locale.patch

# fedora patches
Patch101:	file-5.18-strength.patch
Patch103:	file-4.17-rpm-name.patch
Patch104:	file-5.04-volume_key.patch
Patch105:	file-5.04-man-return-code.patch
Patch106:	file-5.04-generic-msdos.patch
Patch107:	file-5.18-x86boot.patch
Patch108:	file-5.18-perl.patch
Patch111:	file-5.18-no-magic.patch
Patch112:	file-5.18-journald.patch

BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(zlib)
%if %{with uclibc}
BuildRequires:	uClibc-devel
BuildRequires:	uclibc-zlib-devel
%endif
Requires:       %{libname} = %{EVRD}

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%if %{with uclibc}
%package -n	uclibc-%{name}
Summary:	A utility for determining file types (uClibc build)
Group:		File tools
Requires:	%{name} = %{EVRD}

%description -n	uclibc-%{name}
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.
%endif

%package -n	%{libname}
Summary:	Shared library for handling magic files
Group:		System/Libraries

%description -n	%{libname}
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	Shared library for handling magic files (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

%package -n	uclibc-%{devname}
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	uclibc-%{libname} = %{EVRD}
Provides:	uclibc-magic-devel = %{EVRD}
Conflicts:	%{devname} < 5.23-2

%description -n	uclibc-%{devname}
This package contains the development files for %{name}.
%endif

%package -n	%{devname}
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	magic-devel = %{EVRD}

%description -n	%{devname}
This package contains the development files for %{name}.

%package -n	%{static}
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	magic-static-devel = %{EVRD}

%description -n	%{static}
This package contains the static library for %{name}.

%package -n	python-magic
Summary:	Python module to use libmagic
Group:		Development/Python
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description -n	python-magic
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

This package contains the python binding for libmagic.

%package -n	python2-magic
Summary:	Python 2.x module to use libmagic
Group:		Development/Python
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

%description -n	python2-magic
Libmagic is a library for handlig the so called magic files the 'file'
command is based on. 

This package contains the python 2.x binding for libmagic.

%prep
%setup -q
%apply_patches

autoreconf -fi
find -name .0*~ -delete

%build
export CONFIGURE_TOP="$PWD"
%global optflags %{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
mkdir -p glibc
pushd glibc
%configure --enable-static
# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make
popd

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure
# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make
popd
%endif

cd python
python setup.py build
cd -


%install
%makeinstall_std -C glibc
mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libmagic.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libmagic.so.%{major}.*.* %{buildroot}%{_libdir}/libmagic.so

%if %{with uclibc}
%makeinstall_std -C uclibc
mkdir %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libmagic.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -srf %{buildroot}%{uclibc_root}/%{_lib}/libmagic.so.%{major}.*.* %{buildroot}%{uclibc_root}%{_libdir}/libmagic.so
%endif

# install one missing header file
install -m644 src/file.h -D %{buildroot}%{_includedir}/file.h

pushd python
python setup.py install --prefix=%{buildroot}%{_prefix}

python2 setup.py build
python2 setup.py install --prefix=%{buildroot}%{_prefix}
popd

%files
%doc README MAINT ChangeLog
%{_bindir}/*
%{_datadir}/misc/*
%{_mandir}/man1/*
%{_mandir}/man4/*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_bindir}/*
%endif

%files -n %{libname}
/%{_lib}/libmagic.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libmagic.so.%{major}*

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libmagic.so
%endif

%files -n %{devname}
%{_libdir}/libmagic.so
%{_includedir}/*
%{_mandir}/man3/*

%files -n %{static}
%{_libdir}/libmagic.a

%files -n python-magic
%doc python/README python/example.py
%{py_puresitedir}/*

%files -n python2-magic
%doc python/README python/example.py
%{py2_puresitedir}/*
