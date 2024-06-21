%define debug_package %{nil}

Summary:        Rust reimplementation of GNU core utilities
Name:           rust-coreutils
Version:        0.0.26
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/uutils/coreutils
# Below is a manually created tarball with no download link.
Source0:        rust-coreutils-0.0.26-cargo.tar.gz
Source1:        cargo_config
Source2:        %{url}/archive/refs/tags/v%{version}.tar.gz#/coreutils-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
Conflicts:      coreutils

%description
This package provides the reimplementation of the GNU core utilities in Rust.

%prep
%setup -q -n rust-coreutils
ls
tar -xzf %{SOURCE0}
ls
install -D %{SOURCE1} .cargo/config

%build
cargo build --release


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp target/release/coreutils %{buildroot}%{_bindir}



utilities=(
    "uniq" "nl" "echo" "shred" "od" "basename" "cat" "split" "md5sum" "shake256sum"
    "tr" "dir" "comm" "pwd" "tee" "head" "ls" "sort" "b3sum" "b2sum"
    "printf" "vdir" "test" "dd" "cut" "df" "shuf" "csplit" "ln"
    "numfmt" "mv" "mktemp" "yes" "pr" "seq" "tail" "sha1sum" "sha224sum"
    "touch" "tac" "basenc" "rmdir" "paste" "sha256sum" "sha3-256sum"
    "dirname" "base32" "factor" "printenv" "sleep" "readlink" "sha3-224sum"
    "du" "truncate" "more" "dircolors" "link" "date" "sum" "false"
    "true" "wc" "mkdir" "expand" "hashsum" "sha3-384sum" "sha512sum"
    "cksum" "base64" "unlink" "fold" "expr" "join" "rm" "sha3-512sum" "shake128sum"
    "ptx" "realpath" "unexpand" "fmt" "env" "tsort" "cp" "sha384sum" "sha3sum"
)


pushd %{buildroot}%{_bindir}
for util in "${utilities[@]}"; do 
    ln -sf coreutils ${util}
done
popd

%files
/usr/bin/coreutils
/usr/bin/b2sum
/usr/bin/b3sum
/usr/bin/base32
/usr/bin/base64
/usr/bin/basename
/usr/bin/basenc
/usr/bin/cat
/usr/bin/cksum
/usr/bin/comm
/usr/bin/cp
/usr/bin/csplit
/usr/bin/cut
/usr/bin/date
/usr/bin/dd
/usr/bin/df
/usr/bin/dir
/usr/bin/dircolors
/usr/bin/dirname
/usr/bin/du
/usr/bin/echo
/usr/bin/env
/usr/bin/expand
/usr/bin/expr
/usr/bin/factor
/usr/bin/false
/usr/bin/fmt
/usr/bin/fold
/usr/bin/hashsum
/usr/bin/head
/usr/bin/join
/usr/bin/link
/usr/bin/ln
/usr/bin/ls
/usr/bin/md5sum
/usr/bin/mkdir
/usr/bin/mktemp
/usr/bin/more
/usr/bin/mv
/usr/bin/nl
/usr/bin/numfmt
/usr/bin/od
/usr/bin/paste
/usr/bin/pr
/usr/bin/printenv
/usr/bin/printf
/usr/bin/ptx
/usr/bin/pwd
/usr/bin/readlink
/usr/bin/realpath
/usr/bin/rm
/usr/bin/rmdir
/usr/bin/seq
/usr/bin/sha1sum
/usr/bin/sha224sum
/usr/bin/sha256sum
/usr/bin/sha3-224sum
/usr/bin/sha3-256sum
/usr/bin/sha3-384sum
/usr/bin/sha3-512sum
/usr/bin/sha384sum
/usr/bin/sha3sum 
/usr/bin/sha512sum
/usr/bin/shake128sum
/usr/bin/shake256sum
/usr/bin/shred
/usr/bin/shuf
/usr/bin/sleep
/usr/bin/sort
/usr/bin/split
/usr/bin/sum
/usr/bin/tac
/usr/bin/tail
/usr/bin/tee
/usr/bin/test
/usr/bin/touch
/usr/bin/tr
/usr/bin/true
/usr/bin/truncate
/usr/bin/tsort
/usr/bin/unexpand
/usr/bin/uniq
/usr/bin/unlink
/usr/bin/vdir
/usr/bin/wc
/usr/bin/yes

%changelog 
* Fri May 31 2024 Antonio Salinas ansalinas@microsoft.com - 0.0.26
    - First Rust package reimplementation

