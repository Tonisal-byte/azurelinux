%define debug_package %{nil}

Summary:        Rust shell implementation
Name:           brush-shell
Version:        0.1.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/reubeno/brush
# Below is a manually created tarball with no download link.
Source0:        brush-shell-0.1.0-cargo.tar.gz
Source1:        cargo_config
Source2:        https://github.com/reubeno/brush/archive/refs/tags/brush-brush-shell-v0.1.0.tar.gz

BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  glibc
Provides:       /bin/sh
Provides:     bash

%description
This package provides a rust shell script.

%prep
# Make sure  v $package_name$ v
%setup -q -n brush-shell
tar -xzf %{SOURCE0}
mkdir -p .cargo
install -D %{SOURCE1} .cargo/config


%build
#cargo build --release --offline --manifest-path ./brush-shell/Cargo.toml


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/bin
#cargo install --path . --root %{buildroot}/usr
ls
cp target/release/brush %{buildroot}%{_bindir}
ln -sf ../usr/bin/brush %{buildroot}/bin/sh

#pushd %{buildroot}/usr 
#rm .crates.toml
#rm .crates2.json
#popd

%files
/usr/bin/brush
/bin/sh

%changelog 
* Fri June 14 2024 Antonio Salinas ansalinas@microsoft.com - 0.2.2
    - Rust shell implementation.


