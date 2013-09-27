%define major	1
%define libname	%mklibname magic %{major}
%define devname	%mklibname -d magic
%define staticname %mklibname -d -s magic

Summary:	A utility for determining file types
Name:		file
Version:	5.15
Release:	1
License:	BSD 
Group:		File tools
Url:		http://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Patch3:		file-4.24-selinux.patch
Patch4:		file-5.04-oracle.patch
Patch7:		file-5.05-dump.patch
Patch8:		file-5.10-berkeleydb.patch
Patch9:		file-5.14-xen.patch
Patch13:	file-5.05-images.patch
Patch14:	file-4.20-apple.patch
Patch26:	file-rpm-locale.patch

BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(zlib)

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%package -n	%{libname}
Summary:	Shared library for handling magic files
Group:		System/Libraries

%description -n	%{libname}
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

%package -n	%{devname}
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	magic-devel = %{EVRD}

%description -n	%{devname}
This package contains the development files for %{name}.

%package -n	%{staticname}
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	magic-static-devel = %{EVRD}

%description -n	%{staticname}
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

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure2_5x --enable-static

# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

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

