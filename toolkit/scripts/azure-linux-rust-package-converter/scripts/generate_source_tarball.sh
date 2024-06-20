#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PKG_NAME=""

# parameters:
#
# --srcTarball  : src tarball file
#                 this file contains the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
# --pkgName     : package name 
#
PARAMS=""
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgName)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_NAME=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

echo "--srcTarball   -> $SRC_TARBALL"
echo "--outFolder    -> $OUT_FOLDER"
echo "--pkgVersion   -> $PKG_VERSION"
echo "--pkgName      -> $PKG_NAME"

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf $tmpdir
}
trap cleanup EXIT

TARBALL_FOLDER="$tmpdir/tarballFolder"
mkdir -p $TARBALL_FOLDER
cp $SRC_TARBALL $tmpdir

pushd $tmpdir > /dev/null

NAME_VER="$PKG_NAME-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$NAME_VER-vendored.tar.gz"

echo "Unpacking source tarball..."
mkdir $PKG_NAME
tar -xzf $SRC_TARBALL -C $PKG_NAME --strip-components=1


echo "Vendor cargo ..."
cd $PKG_NAME

#TODO: installing rust as auto-patcher does not have it installed by default. Possibly remove if auto-patcher will be changed to have rust included.
sudo tdnf install -y rust
mkdir -p .cargo
cargo vendor 
ls
echo "

[source.crates-io]
replace-with = \"vendored-sources\"

[source.vendored-sources]
directory = \"vendor\"

" >> .cargo/config.toml

echo ""
echo "========================="
echo "Tar vendored tarball"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -czf "$VENDOR_TARBALL" .

popd > /dev/null
echo "$PKG_NAME vendored modules are available at $VENDOR_TARBALL and static assets in $STATIC_ASSETS_TARBALL"