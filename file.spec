%define	major 1
%define	libname %mklibname magic %{major}
%define	devname %mklibname -d magic
%define	static %mklibname -d -s magic

Summary:	A utility for determining file types
Name:		file
Version:	5.26
Release:	2
License:	BSD
Group:		File tools
Url:		http://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch3:		file-4.24-selinux.patch
Patch4:		file-5.04-oracle.patch
Patch7:		file-5.05-dump.patch
Patch8:		file-5.15-berkeleydb.patch
Patch9:		file-5.14-xen.patch
Patch13:	file-5.05-images.patch
Patch14:	file-4.20-apple.patch
Patch26:	file-rpm-locale.patch

# fedora patches
# (tpg) this patch is prolly merged
#Patch101:	file-5.18-strength.patch
Patch103:	file-4.17-rpm-name.patch
Patch104:	file-5.04-volume_key.patch
Patch105:	file-5.04-man-return-code.patch
# (tpg) this patch is prolly merged
#Patch106:	file-5.04-generic-msdos.patch
Patch107:	file-5.18-x86boot.patch
Patch108:	file-5.18-perl.patch
# (tpg) this patch is prolly merged
#Patch111:	file-5.18-no-magic.patch
Patch112:	file-5.18-journald.patch

BuildRequires:	pkgconfig(python2)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3egg(setuptools)
BuildRequires:	pythonegg(setuptools)
BuildRequires:	pkgconfig(zlib)
Requires:       %{libname} = %{EVRD}

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
cp -a python python2

%build
%global optflags %{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE

%configure --enable-static
# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

pushd python
PYTHONPATH=%{py3_puresitedir} %{__python} setup.py build
popd

pushd python2
PYTHONPATH=%{py2_puresitedir} %{__python2} setup.py build
popd

%install
%makeinstall_std
mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libmagic.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libmagic.so.%{major}.*.* %{buildroot}%{_libdir}/libmagic.so


# install one missing header file
install -m644 src/file.h -D %{buildroot}%{_includedir}/file.h

pushd python
mkdir -p %{buildroot}%{py3_puresitedir}
PYTHONPATH=%{buildroot}%{py3_puresitedir} %{__python} setup.py install -O1 --skip-build --root=%{buildroot}
popd

pushd python2
# (tpg) build py2
mkdir -p %{buildroot}%{py2_puresitedir}
PYTHONPATH=%{buildroot}%{py2_puresitedir} %{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
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

%files -n %{static}
%{_libdir}/libmagic.a

%files -n python-magic
%doc python/README python/example.py
%{py_puresitedir}/*

%files -n python2-magic
%doc python/README python/example.py
%{py2_puresitedir}/*
