
#!/bin/bash
#
# Installs the specified <hh-suite HHM database> in the <remote directory> to <target directory>.

# exit immediately if any command fails
set -e 

DB_NAME=$1
TARGET_DIR=$2

ROOT_URL="http://wwwuser.gwdg.de/~compbiol/uniclust/2017_10"

if [[ -z "$DB_NAME" || -z "$TARGET_DIR" ]]; then
	echo "Usage: $0 <db name> <target directory>"
	exit 1
fi


HHM_URL="$ROOT_URL/$DB_NAME"
EMPTY_STR=""
HHM_BASE_NAME="${DB_NAME/.tgz/$EMPTY_STR}"
HHM_BASE_NAME="${HHM_BASE_NAME/.tar.gz/$EMPTY_STR}"
HHM_BASE_NAME="${HHM_BASE_NAME/_hhsuite/$EMPTY_STR}"
TMP=$TARGET_DIR/tmp
mkdir -p $TMP

if [[ -s "$TARGET_DIR/$HHM_BASE_NAME" ]]; then
	echo "$HHM_BASE_NAME database is already installed"
	exit 
fi

if [[ ! -s "$TARGET_DIR/$HHM_BASE_NAME" ]]; then
	echo "Downloading Uniclust database $HHM_BASE_NAME"
	# wget --no-verbose -O "$TMP/$DB_NAME" $HHM_URL
	wget -O "$TMP/$DB_NAME" $HHM_URL
	echo "Decompressing"
    mkdir -p "$TARGET_DIR/$HHM_BASE_NAME"
	tar -xzf "$TMP/$DB_NAME" -C "$TARGET_DIR/$HHM_BASE_NAME"
fi

echo "Cleaning up"
rm -rf $TMP

echo "Successfully installed HH-suite $HHM_BASE_NAME database"