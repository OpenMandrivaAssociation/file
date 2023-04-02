%define major 1
%define libname %mklibname magic %{major}
%define devname %mklibname -d magic
%define static %mklibname -d -s magic

Summary:	A utility for determining file types
Name:		file
Version:	5.44
Release:	2
License:	BSD
Group:		File tools
Url:		https://www.darwinsys.com/file/
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Patch4:		file-5.04-oracle.patch
Patch8:		file-5.15-berkeleydb.patch
Patch9:		file-5.14-xen.patch
#Patch26:	file-rpm-locale.patch

# Fedora patches
Patch103:	file-4.17-rpm-name.patch
Patch104:	file-5.04-volume_key.patch

BuildRequires:	pkgconfig(python3)
BuildRequires:	python3egg(setuptools)
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

%prep
%autosetup -p1

autoreconf -fi
find -name .0*~ -delete

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

%install
%make_install

# install one missing header file
install -m644 src/file.h -D %{buildroot}%{_includedir}/file.h

cat magic/Magdir/* > %{buildroot}%{_datadir}/misc/magic

cd python
mkdir -p %{buildroot}%{py3_puresitedir}
PYTHONPATH=%{buildroot}%{py3_puresitedir} %{__python} setup.py install -O1 --skip-build --root=%{buildroot}
cd ..

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

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
