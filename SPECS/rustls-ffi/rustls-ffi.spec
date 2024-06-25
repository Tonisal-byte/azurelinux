%define debug_package %{nil}

Summary:        Rustls API (C) used to interface with rust implemented tls
Name:           rustls-ffi
Version:        0.10.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rustls/rustls-ffi
# Below is a automatically created tarball with no download link.
Source0:        rustls-ffi-0.10.0-vendored.tar.gz
Source1: 	    %{url}/archive/refs/tags/v%{version}.tar.gz#/rustls-ffi-0.13.0.tar.gz

# Required build packages
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  glibc
Requires:       rust
#FILL IN THE REST OF THE PACKAGES BELOW IF NEEDED. (Consult package docs)


%description
Rustls API (C) used to interface with rust implemented tls

%prep
%setup -q -n %{name}-%{version}
tar -xzf %{SOURCE0}

%build
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib/rustls-ffi
make DESTDIR=%{buildroot}/usr/lib/rustls-ffi install


# FILL IN FILES INCLUDED IN PKG (Ex: /usr/bin/{YOUR BINARY})
%files
/usr/lib/rustls-ffi/lib/librustls.a
/usr/lib/rustls-ffi/include/rustls.h

%changelog 

* Mon Jun 24 2024 Antonio Salinas <t-ansalinas@microsoft.com> - 0.10.0
- Rust implementation of tls procol

