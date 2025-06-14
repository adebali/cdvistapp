#!/bin/bash

set -e 

VERSION=$1
TARGET_DIR=$2
MAKE_PROFILE_SCRIPT_DIR=$3

if [[ -z "$VERSION" || -z "$TARGET_DIR" || -z "$MAKE_PROFILE_SCRIPT_DIR" ]]; then
	echo "Usage: $0 <bitscore version> <target directory> <blast makeprofiledb bin>"
	exit 1
fi

if [[ ! $VERSION =~ ^[1-9]*\.[0-9][0-9]$ ]] ; then
	echo 'Missing or invalid version!'
	exit 1
fi

CDD_PSSM_NAME="cdd"
GZ_CDD_PSSM_NAME="$CDD_PSSM_NAME.tar.gz"

BITSCORE_SPECIFIC_FILE="bitscore_specific_$VERSION.txt"
CDD_PSSM_URL="ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.tar.gz"
BITSCORE_SPECIFIC_URL="ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/$BITSCORE_SPECIFIC_FILE"


if [[ -s "$TARGET_DIR/$BITSCORE_SPECIFIC_FILE" ]]; then
	echo "CDD Specific Bitscore $VERSION is already downloaded"
else
    wget --no-verbose -O $TARGET_DIR/$BITSCORE_SPECIFIC_FILE $BITSCORE_SPECIFIC_URL
    echo "Successfully fetched CDD PSSM bitscore specific file version $VERSION"
fi

if [[ -s "$TARGET_DIR/Cdd_NCBI.rps" ]]; then
	echo "CDD PSSM database is already downloaded"
    exit
fi

echo "Downloading CDD PSSM database"
wget --no-verbose -O "$TARGET_DIR/$GZ_CDD_PSSM_NAME" $CDD_PSSM_URL
echo "Decompressing"
mkdir -p $TARGET_DIR/cdd
tar xzf "$TARGET_DIR/$GZ_CDD_PSSM_NAME" -C "$TARGET_DIR/cdd"


cd $TARGET_DIR/cdd
echo "Making profile (PSSM) databases of CDD, COG, KOG, Pfam, Prk, Smart, Tigr"
makeprofiledb -title Cdd_NCBI -in Cdd_NCBI.pn -out ../Cdd_NCBI -threshold 9.82 -scale 100.0 -dbtype rps -index true
makeprofiledb -title Cog -in Cog.pn -out ../Cog -threshold 9.82 -scale 100.0 -dbtype rps -index true
makeprofiledb -title Kog -in Kog.pn -out ../Kog -threshold 9.82 -scale 100.0 -dbtype rps -index true
makeprofiledb -title Pfam -in Pfam.pn -out ../Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true
makeprofiledb -title Prk -in Prk.pn -out ../Prk -threshold 9.82 -scale 100.0 -dbtype rps -index true
makeprofiledb -title Smart -in Smart.pn -out ../Smart -threshold 9.82 -scale 100.0 -dbtype rps -index true
makeprofiledb -title Tigr -in Tigr.pn -out ../Tigr -threshold 9.82 -scale 100.0 -dbtype rps -index true

echo "Cleaning up"
cd ..
rm "$TARGET_DIR/$GZ_CDD_PSSM_NAME"

echo "Successfully fetched CDD PSSM database database"