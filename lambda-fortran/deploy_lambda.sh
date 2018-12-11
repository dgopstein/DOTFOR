BASE_DIR=`pwd`
BASE_NAME=$(basename $BASE_DIR)

BUILD_DIR=$BASE_DIR/build

ZIP_DIR=$BUILD_DIR/zip
ZIP_FILE=$ZIP_DIR/$BASE_NAME.zip

STAGING_DIR=$BUILD_DIR/$BASE_NAME

set -o xtrace

: "Removing staging dir: " $STAGING_DIR
rm -r $STAGING_DIR

: "Removing old zip: " $ZIP_FILE
rm $ZIP_FILE

mkdir -p $STAGING_DIR
mkdir -p $ZIP_DIR

: "Extracting g95 archive to staging dir... "
tar -xJf $BASE_DIR/g95.tar.xz -C $STAGING_DIR

: "Copying ruby code to staging dir..."
cp $BASE_DIR/*.rb $STAGING_DIR/

cd $BUILD_DIR

: "Uploading code to AWS..."
zip -r $ZIP_FILE $BASE_NAME -x build/* -x .* -x *~ &&
    aws lambda update-function-code --profile personal --function-name arn:aws:lambda:us-east-1:239445984846:function:dotfor --zip-file fileb://$ZIP_FILE
