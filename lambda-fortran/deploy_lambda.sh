BASEDIR=$(dirname "$0")

rm $BASEDIR/build/lambda-fortran.zip

zip -r $BASEDIR/build/lambda-fortran.zip $BASEDIR -x build/* -x .* &&
    aws lambda update-function-code --profile personal --function-name arn:aws:lambda:us-east-1:239445984846:function:dotfor --zip-file fileb://$BASEDIR/build/lambda-fortran.zip
