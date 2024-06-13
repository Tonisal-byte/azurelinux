%define debug_package %{nil}

Summary:        Rust reimplementation of sudo and su
Name:           rust-sudo
Version:        0.2.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/memorysafety/sudo-rs
# Below is a manually created tarball with no download link.
Source0:        rust-sudo-0.2.2-cargo.tar.gz
Source1:        cargo_config
Source2:        %{url}/archive/refs/tags/v%{version}.tar.gz#/sudo-rs-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
BuildRequires:  pam-devel

#Requires:       audit-libs
#Requires:       bash
#Requires:       cracklib
#Requires:       cracklib-dicts
#Requires:       glibc
#Requires:       libcap-ng
#Requires:       openldap
#Requires:       openssl-libs   
#Requires:       pam
#Requires:       shadow-utils 
#Requires:       zlib

%description
This package provides the reimplementation of sudo and su.

%prep
%setup -q -n rust-sudo
tar -xzf %{SOURCE0}
install -D %{SOURCE1} .cargo/config

%build
cargo build --release --offline

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp target/release/sudo %{buildroot}%{_bindir}
cp target/release/su %{buildroot}%{_bindir}
chown root:root %{buildroot}%{_bindir}/sudo
chown root:root %{buildroot}%{_bindir}/su

%files
/usr/bin/sudo
/usr/bin/su

%changelog 
* Wed June 12 2024 Antonio Salinas ansalinas@microsoft.com - 0.2.2
    - Rust sudo and su reimplementation.


