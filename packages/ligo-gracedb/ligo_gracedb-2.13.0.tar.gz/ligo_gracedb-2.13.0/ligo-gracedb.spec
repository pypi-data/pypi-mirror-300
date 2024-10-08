%define srcname           ligo-gracedb
%define distname          ligo_gracedb
%define version           2.13.0
%define unmangled_version 2.13.0
%define release           1

Summary:   Gravity Wave Candidate Event Database
Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Source0:   %pypi_source %distname
License:   GPLv3+
Prefix:    %{_prefix}
Vendor:    Tanner Prestegard <tanner.prestegard@ligo.org>, Alexander Pace <alexander.pace@ligo.org>, Duncan Meacher <duncan.meacher@ligo.org>
Url:       https://ligo-gracedb.readthedocs.io/en/latest/

BuildArch: noarch

# srpm dependencies:
BuildRequires: python-srpm-macros

# build dependencies: python3, setuptools, wheel
BuildRequires: python%{python3_pkgversion}-devel >= 3.6
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-wheel


%description
The gravitational-wave candidate event database (GraceDB) is a
system to organize candidate events from gravitational-wave searches and
to provide an environment to record information about follow-ups.

# -- python-3X-ligo-gracedb

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  Python %{python3_version} client library for GraceDB
Requires: python%{python3_pkgversion}-cryptography
Requires: python%{python3_pkgversion}-future
Requires: python%{python3_pkgversion}-igwn-auth-utils >= 1.0.0
Requires: python%{python3_pkgversion}-requests
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
The gravitational-wave candidate event database (GraceDB) is a
system to organize candidate events from gravitational-wave searches and
to provide an environment to record information about follow-ups.
This package provides the %{python3_version} library.

# -- ligo-gracedb

%package -n %{srcname}
Summary: Command-line interface for GraceDB
Requires: python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
Obsoletes: python2-ligo-gracedb <= 2.7.6-1.1
%description -n %{srcname}
The gravitational-wave candidate event database (GraceDB) is a
system to organize candidate events from gravitational-wave searches and
to provide an environment to record information about follow-ups.
This package provides the command-line client tool.

# -- build steps

%prep
%autosetup -n %{distname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel ligo_gracedb-%{version}-*.whl

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/*

%files -n %{srcname}
%doc README.rst
%license LICENSE
%{_bindir}/gracedb

%changelog
* Wed Jun 12 2019 Duncan Macleod <duncan.macleod@ligo.org> 2.2.2-2
- fixed incorrect installation of /usr/bin/ scripts
- cleaned up spec file
