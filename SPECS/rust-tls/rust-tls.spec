Summary:        An SSL libaray implemented in Rust 
Name:           rust-tls
Version:        0.23.10
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rustls/rustls
# Below is a automatically created tarball with no download link.
Source0:	    rust-tls-0.23.10-vendored.tar.gz
Source1: 	    %{url}/archive/refs/tags/v%{version}.tar.gz#/rustls-v-0.23.10.tar.gz

# Required build packages
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
#FILL IN THE REST OF THE PACKAGES BELOW IF NEEDED. (Consult package docs)


%description
An SSL libaray implemented in Rust. For use in curl package.

%prep
%setup -q -n %{name}
tar -xzf %{SOURCE0}

%build
cargo build --release --offline --manifest-path ./rustls/Cargo.toml

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib %{buildroot}/usr/include/rust-tls
cargo install --path ./rustls --root %{buildroot}/usr
pushd %{buildroot}/usr 
rm .crates.toml
rm .crates2.json
popd

# FILL IN FILES INCLUDED IN PKG (Ex: /usr/bin/{YOUR BINARY})
%files
/usr/include/rust-tls/*
/usr/lib/librustls.so

# FILL IN INITAL COMMIT LOG
%changelog 

* Mon June 23 2024 Antonio Salinas ansalinas@microsoft.com - 0.23.10
    - Rust ssl library.



