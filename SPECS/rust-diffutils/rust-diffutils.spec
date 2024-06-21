%define debug_package %{nil}

Summary:        Rust reimplementation of diff utils
Name:           rust-diffutils
Version:        0.4.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/uutils/diffutils/
# Below is a automatically created tarball with no download link.
Source0:    rust-diffutils-0.4.1-vendored.tar.gz
Source1: 	%{url}/archive/refs/tags/v%{version}.tar.gz#/diffutils-0.4.1.tar.gz

# Required build packages
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
#FILL IN THE REST OF THE PACKAGES BELOW IF NEEDED. (Consult package docs)


%description
Rust reimplementation of diff utils

%prep
%setup -q -n %{name}
tar -xzf %{SOURCE0}

%build
cargo build --release --offline

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/bin
cargo install --path . --root %{buildroot}/usr
ln -sf diffutils %{buildroot}/bin/diff
pushd %{buildroot}/usr 
rm .crates.toml
rm .crates2.json
popd

# FILL IN FILES INCLUDED IN PKG (Ex: /usr/bin/{YOUR BINARY})
%files
/usr/bin/diffutils
/bin/diff

# FILL IN INITAL COMMIT LOG
%changelog 
* Fri June 21 2024 Antonio Salinas ansalinas@microsoft.com - 0.4.1
    - Rust implementation of diff (utility).


