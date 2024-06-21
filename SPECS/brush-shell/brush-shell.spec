%define debug_package %{nil}

Summary:        Rust shell implementation
Name:           brush-shell
Version:        0.2.2
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/reubeno/brush
# Below is a manually created tarball with no download link.
Source0:        brush-shell-0.2.2-vendored.tar.gz
Source1:        %{url}/archive/refs/tags/v%{version}.tar.gz#/brush-brush-shell-v0.2.2.tar.gz

BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  glibc
Provides:       /bin/sh
Provides:        /bin/bash
Conflicts:      bash

%description
This package provides a rust shell script.

%prep
%setup -q -n %{name}
tar -xzf %{SOURCE0}

%build
ls
cargo build --release --offline
#cargo build --release --offline --manifest-path ./brush-shell/Cargo.toml


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/bin
cargo install --path ./brush-shell --root %{buildroot}/usr
ln -sf brush %{buildroot}/bin/sh
ln -sf brush %{buildroot}/bin/bash

pushd %{buildroot}/usr 
rm .crates.toml
rm .crates2.json
popd

%files
/usr/bin/brush
/bin/sh
/bin/bash

%changelog 
* Wed June 19 2024 Antonio Salinas ansalinas@microsoft.com - 0.2.2
    - Now builds using source code instead of copying precompiled binary.

* Fri June 14 2024 Antonio Salinas ansalinas@microsoft.com - 0.1.0
    - Rust shell implementation.


