#!/bin/bash
#
# Installs the specified Pfam <database version> to <target directory>. Assumes
# that the hmmpress binary (part of HMMER3) is  in the $PATH environment variable. 

# exit immediately if any command fails
set -e 

VERSION=$1
TARGET_DIR=$2

mkdir -p $TARGET_DIR/$VERSION
TARGET_DIR=$TARGET_DIR/$VERSION

if [[ -z "$VERSION" || -z "$TARGET_DIR" ]]; then
	echo "Usage: $0 <pfam version> <target directory>"
	exit 1
fi

if [[ ! $VERSION =~ ^[1-9][0-9]*\.[0-9]$ ]] ; then
	echo 'Missing or invalid version!'
	exit 1
fi

PFAM_HMM_NAME="Pfam-A.hmm"
GZ_PFAM_HMM_NAME="$PFAM_HMM_NAME.gz"
PFAM_HMM_URL="ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam$VERSION/$GZ_PFAM_HMM_NAME"
TMP=$TARGET_DIR/tmp
mkdir -p $TMP

if [[ -s "$TARGET_DIR/$PFAM_HMM_NAME" &&
	-s "$TARGET_DIR/$PFAM_HMM_NAME.h3f" &&
	-s "$TARGET_DIR/$PFAM_HMM_NAME.h3i" &&
	-s "$TARGET_DIR/$PFAM_HMM_NAME.h3m" &&
	-s "$TARGET_DIR/$PFAM_HMM_NAME.h3p" ]]; then
	echo "Pfam $VERSION database is already installed"
	exit 
fi

if [[ ! -s "$TARGET_DIR/$PFAM_HMM_NAME" ]]; then
	echo "Downloading HMM database"
	# wget --no-verbose -O "$TMP/$GZ_PFAM_HMM_NAME" $PFAM_HMM_URL
	wget -O "$TMP/$GZ_PFAM_HMM_NAME" $PFAM_HMM_URL
	echo "Decompressing"
	gunzip "$TMP/$GZ_PFAM_HMM_NAME"
	echo "Copying to $TARGET_DIR"
	mkdir -p $TARGET_DIR
	mv "$TMP/$PFAM_HMM_NAME" $TARGET_DIR
fi

cd $TARGET_DIR
echo "Preparing Pfam HMM database"
hmmpress -f ./$PFAM_HMM_NAME

echo "Cleaning up"
rm -rf $TMP

echo "Successfully installed Pfam $VERSION database"
