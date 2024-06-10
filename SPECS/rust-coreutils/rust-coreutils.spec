%define debug_package %{nil}

Summary:        Rust reimplementation of GNU core utilities
Name:           rust-coreutils
Version:        0.0.26
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/uutils/coreutils
Source0:        coreutils-0.0.26-x86_64-unknown-linux-gnu.tar.gz
Source1:        https://github.com/uutils/coreutils/releases/download/0.0.26/coreutils-0.0.26-x86_64-unknown-linux-gnu.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  glibc
# Requires:       clap
# Requires:       clap_complete
# Requires:       clap_mangen
# Requires:       once_cell
# Requires:       phf
# Requires:       textwrap
# Requires:       uucore



%description
This package provides the reimplementation of the GNU core utilities in Rust.

%prep
%setup -q -n coreutils
tar -xzf %{SOURCE0}

%build
cargo build --release --offline


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp target/release/coreutils %{buildroot}%{_bindir}



utilities=(
    "uniq" "nl" "echo" "shred" "od" "basename" "chown" "cat" "install" "split"
    "chroot" "tr" "dir" "comm" "pwd" "tee" "head" "whoami" "ls" "uname" "sort"
    "who" "printf" "vdir" "hostid" "test" "dd" "cut" "df" "shuf" "csplit" "ln"
    "numfmt" "mv" "mktemp" "yes" "pr" "stdbuf" "mkfifo" "pathchk" "seq" "tail"
    "touch" "tac" "nice" "basenc" "tty" "rmdir" "users" "pinky" "logname" "paste"
    "dirname" "groups" "runcon" "id" "base32" "factor" "printenv" "sleep" "readlink"
    "stat" "du" "truncate" "more" "dircolors" "uptime" "link" "date" "sum" "false"
    "true" "wc" "timeout" "nohup" "stty" "mkdir" "nproc" "chgrp" "expand" "hashsum"
    "cksum" "base64" "unlink" "fold" "expr" "join" "hostname" "rm" "kill" "arch"
    "ptx" "realpath" "mknod" "unexpand" "chcon" "fmt" "chmod" "sync" "env" "tsort" "cp"
)


#mkdir -p %{buildroot}%{_prefix}/local/bin
pushd %{buildroot}%{_bindir}
for util in "${utilities[@]}"; do 
    touch $util
    ln -sf coreutils ${util}
    #touch $util
    #echo -e "#!/bin/sh\n/usr/bin/coreutils $util \"\$@\"" > $util; 
    #chmod +x $util; 
done
popd

%files
/usr/bin/coreutils
/usr/bin/arch
/usr/bin/base32
/usr/bin/base64
/usr/bin/basename
/usr/bin/basenc
/usr/bin/cat
/usr/bin/chcon
/usr/bin/chgrp
/usr/bin/chmod
/usr/bin/chown
/usr/bin/chroot
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
/usr/bin/groups
/usr/bin/hashsum
/usr/bin/head
/usr/bin/hostid
/usr/bin/hostname
/usr/bin/id
/usr/bin/install
/usr/bin/join
/usr/bin/kill
/usr/bin/link
/usr/bin/ln
/usr/bin/logname
/usr/bin/ls
/usr/bin/mkdir
/usr/bin/mkfifo
/usr/bin/mknod
/usr/bin/mktemp
/usr/bin/more
/usr/bin/mv
/usr/bin/nice
/usr/bin/nl
/usr/bin/nohup
/usr/bin/nproc
/usr/bin/numfmt
/usr/bin/od
/usr/bin/paste
/usr/bin/pathchk
/usr/bin/pinky
/usr/bin/pr
/usr/bin/printenv
/usr/bin/printf
/usr/bin/ptx
/usr/bin/pwd
/usr/bin/readlink
/usr/bin/realpath
/usr/bin/rm
/usr/bin/rmdir
/usr/bin/runcon
/usr/bin/seq
/usr/bin/shred
/usr/bin/shuf
/usr/bin/sleep
/usr/bin/sort
/usr/bin/split
/usr/bin/stat
/usr/bin/stdbuf
/usr/bin/stty
/usr/bin/sum
/usr/bin/sync
/usr/bin/tac
/usr/bin/tail
/usr/bin/tee
/usr/bin/test
/usr/bin/timeout
/usr/bin/touch
/usr/bin/tr
/usr/bin/true
/usr/bin/truncate
/usr/bin/tsort
/usr/bin/tty
/usr/bin/uname
/usr/bin/unexpand
/usr/bin/uniq
/usr/bin/unlink
/usr/bin/uptime
/usr/bin/users
/usr/bin/vdir
/usr/bin/wc
/usr/bin/who
/usr/bin/whoami
/usr/bin/yes

%changelog 
* Fri May 31 2024 Antonio Salinas ansalinas@microsoft.com - 0.0.26
    - First Rust package reimplementation

