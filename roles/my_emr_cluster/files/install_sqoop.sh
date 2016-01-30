#!/bin/bash -ex

SQOOP_S3_URL=$1
PG_JDBC_S3_URL=$2
DEST_DIR=$HOME
SQOOP_DIST_FILENAME=$(basename $SQOOP_S3_URL)
PG_JDBC_DIST_FILENAME=$(basename $PG_JDBC_S3_URL)
SQOOP_ENV_SCRIPT=/etc/profile.d/sqoop.sh
SQOOP_HOME_DIR=$DEST_DIR/$(basename $SQOOP_DIST_FILENAME .tar.gz)

cd $DEST_DIR
aws s3 cp $SQOOP_S3_URL $DEST_DIR/
tar -xzf $SQOOP_DIST_FILENAME

aws s3 cp $PG_JDBC_S3_URL $SQOOP_HOME_DIR/lib/

sudo touch $SQOOP_ENV_SCRIPT
sudo chmod 777 $SQOOP_ENV_SCRIPT
echo "export PATH=\"\$PATH:$SQOOP_HOME_DIR/bin\"" >> $SQOOP_ENV_SCRIPT
