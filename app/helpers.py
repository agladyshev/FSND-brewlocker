from flask import current_app, flash
from . import s3


def uploadToS3(file, bucket_name, acl="public-read"):
    # backup upload method
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
