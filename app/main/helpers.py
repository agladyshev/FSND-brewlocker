from flask import current_app, flash
import boto3
import botocore

s3 = boto3.client(
    "s3",
    aws_access_key_id=current_app.config['S3_KEY'],
    aws_secret_access_key=current_app.config['S3_SECRET']
)


def uploadToS3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        flash("Upload error")
        return e
    return "{}{}".format(current_app.config['S3_LOCATION'], file.filename)
