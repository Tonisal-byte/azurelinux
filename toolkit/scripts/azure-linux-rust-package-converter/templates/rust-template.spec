Summary:        # FILL IN SUMMARY
Name:           # FILL IN NAME OF PACKAGE (i.e. name listed in distro)
Version:        # FILL IN VERSION
Release:        1%{?dist}
License:        # FILL IN LICENSE
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            # FILL IN URL
# Below is a automatically created tarball with no download link.
Source0:        # DO NOT FILL IN
Source1:        # DO NOT FILL IN

# Required build packages
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
#FILL IN THE REST OF THE PACKAGES BELOW IF NEEDED. (Consult package docs)


%description
# FILL IN DESCRIPTION

%prep
%setup -q -n %{name}
tar -xzf %{SOURCE0}

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

# FILL IN FILES INCLUDED IN PKG (Ex: /usr/bin/{YOUR BINARY})
%files


# FILL IN INITAL COMMIT LOG
%changelog 



