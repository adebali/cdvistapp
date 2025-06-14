#!/bin/bash

set -e

VERSION=$1
TARGET_DIR=$2

if [[ -z "$VERSION" || -z "$TARGET_DIR" ]]; then
	echo "Usage: $0 <blast version> <target directory>"
	exit 1
fi

TARGET_VERSION_DIR=$TARGET_DIR/$VERSION

if [[ -s "$TARGET_VERSION_DIR/bin/rpsblast" ]]; then
	echo "Blast version $VERSION is already installed"
	exit
fi

TARBALL_FILENAME="ncbi-blast-${VERSION}+-x64-linux.tar.gz"
BLAST_URL="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/$VERSION/$TARBALL_FILENAME"
echo "Downloading BLAST tarball"
cd /tmp
wget --no-verbose $BLAST_URL
echo "Decompressing tarball"
tar zxvf $TARBALL_FILENAME

echo "Copying the folder"
mkdir -p $TARGET_VERSION_DIR
cp -r ncbi-blast-$VERSION+/* $TARGET_VERSION_DIR/

echo "Cleaning up"
cd /tmp
rm -r ncbi-blast-$VERSION+

echo "Successfully installed BLAST version $VERSION"
