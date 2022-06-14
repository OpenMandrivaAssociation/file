%define major 1
%define libname %mklibname magic %{major}
%define devname %mklibname -d magic
%define static %mklibname -d -s magic

Summary:	A utility for determining file types
Name:		file
Version:	5.42
Release:	2
License:	BSD
Group:		File tools
Url:		http://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch3:		file-4.24-selinux.patch
Patch4:		file-5.04-oracle.patch
Patch8:		file-5.15-berkeleydb.patch
Patch9:		file-5.14-xen.patch
#Patch26:	file-rpm-locale.patch
Patch10:	file-5.42-fix-size-of-lines-read-from-stdin.patch

# Fedora patches
Patch103:	file-4.17-rpm-name.patch
Patch104:	file-5.04-volume_key.patch

BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-pkg-resources
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3egg(setuptools)
BuildRequires:	python2dist(setuptools)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libseccomp)
Requires:	%{libname} = %{version}

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%package -n %{libname}
Summary:	Shared library for handling magic files
Group:		System/Libraries

%description -n %{libname}
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

%package -n %{devname}
Summary:	Development files to build applications that handle magic files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	magic-devel = %{EVRD}

%description -n %{devname}
This package contains the development files for %{name}.

%package -n %{static}
Summary:	Static library to build applications that handle magic files
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	magic-static-devel = %{EVRD}

%description -n %{static}
This package contains the static library for %{name}.

%package -n python-magic
Summary:	Python module to use libmagic
Group:		Development/Python
BuildArch:	noarch
Provides:	python3-magic = %{version}-%{release}
Requires:	%{name}
Obsoletes:	python-file-magic < 5.39-5

%description -n python-magic
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

This package contains the python binding for libmagic.

%package -n python2-magic
Summary:	Python 2.x module to use libmagic
Group:		Development/Python
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python2-file-magic < 5.39-5

%description -n python2-magic
Libmagic is a library for handlig the so called magic files the 'file'
command is based on.

This package contains the python 2.x binding for libmagic.

%prep
%autosetup -p1

autoreconf -fi
find -name .0*~ -delete
cp -a python python2

%build
# Fix linking libmagic (vfork needs libpthread)
%global optflags %{optflags} -Oz -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -pthread

%configure \
	--enable-static \
	--enable-xzlib \
	--enable-bzlib \
	--enable-zlib \
	--enable-libseccomp

# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

cd python
PYTHONPATH=%{py3_puresitedir} %{__python} setup.py build
cd ..

cd python2
PYTHONPATH=%{py2_puresitedir} %{__python2} setup.py build
cd ..

%install
%make_install

# install one missing header file
install -m644 src/file.h -D %{buildroot}%{_includedir}/file.h

cat magic/Magdir/* > %{buildroot}%{_datadir}/misc/magic

cd python
mkdir -p %{buildroot}%{py3_puresitedir}
PYTHONPATH=%{buildroot}%{py3_puresitedir} %{__python} setup.py install -O1 --skip-build --root=%{buildroot}
cd ..

cd python2
# (tpg) build py2
mkdir -p %{buildroot}%{py2_puresitedir}
PYTHONPATH=%{buildroot}%{py2_puresitedir} %{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
cd ..

%check
if [ $(echo %{_bindir}/file |%{buildroot}%{_bindir}/file -N -f - |cut -d: -f1) != %{_bindir}/file ]; then
	echo "Basic sanity check failed. This is likely to break other package builds."
	exit 1
fi

%files
%doc MAINT
%{_bindir}/*
%{_datadir}/misc/*
%doc %{_mandir}/man1/*
%doc %{_mandir}/man4/*

%files -n %{libname}
%{_libdir}/libmagic.so.%{major}*

%files -n %{devname}
%{_libdir}/libmagic.so
%{_libdir}/pkgconfig/libmagic.pc
%{_includedir}/*
%doc %{_mandir}/man3/*

%files -n %{static}
%{_libdir}/libmagic.a

%files -n python-magic
%{py_puresitedir}/*

%files -n python2-magic
%{py2_puresitedir}/*
