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
Requires:       brush-shell



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
mkdir -p %{buildroot}
cargo install --path . --root %{buildroot}/usr
pushd %{buildroot}/usr 
rm .crates.toml
rm .crates2.json
popd

%files
/usr/bin/sudo
/usr/bin/su
/usr/bin/visudo

%changelog 
* Wed June 12 2024 Antonio Salinas ansalinas@microsoft.com - 0.2.2
    - Rust sudo and su reimplementation.


