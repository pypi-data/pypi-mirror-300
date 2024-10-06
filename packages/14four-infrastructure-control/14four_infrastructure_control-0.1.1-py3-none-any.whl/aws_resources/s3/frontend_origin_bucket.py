import json
import os
from typing import Optional
import mimetypes
from pulumi import Inputs, ResourceOptions
from pulumi_aws import s3
from pydantic import BaseModel
import pulumi


class FrontendOriginBucketArgs:

    content_path: pulumi.Input[str]
    """Path to content for the bucket"""

    @staticmethod
    def from_inputs(inputs: Inputs) -> 'FrontendOriginBucketArgs':
        return FrontendOriginBucketArgs(content_path=inputs['contentPath'])

    def __init__(self, content_path: pulumi.Input[str]) -> None:
        self.content_path = content_path


class FrontendOriginBucket(pulumi.ComponentResource):
    bucket: s3.Bucket
    website_url: pulumi.Output[str]

    def __init__(self,
                 name: str,
                 args: FrontendOriginBucketArgs,
                 props: Optional[dict] = None,
                 opts: Optional[ResourceOptions] = None) -> None:

        super().__init__('s3:index:FrontendOriginBucket', name, props, opts)

        # Create a bucket
        bucket = s3.Bucket(
            f'{name}-bucket',
            website=s3.BucketWebsiteArgs(index_document='index.html'),
            opts=ResourceOptions(parent=self))

        bucket_objects = []
        # Walk through the content directory and upload all files
        for root, directories, files in os.walk(args.content_path):
            for file in files:
                file_path = os.path.join(root, file)

                # Determine the key relative to the content_path
                relative_key = os.path.relpath(file_path, args.content_path).replace("\\", "/")

                # If the file is directly under content_path, keep it in the root of the bucket
                if os.path.dirname(relative_key) == ".":
                    relative_key = file  # Place the file at the root of the S3 bucket

                # Guess the MIME type based on the file extension
                content_type, _ = mimetypes.guess_type(file_path)

                # Default to 'binary/octet-stream' if MIME type cannot be determined
                if content_type is None:
                    content_type = 'binary/octet-stream'

                # Create the BucketObject with the correct key and content type
                bucket_objects.append(
                    s3.BucketObject(
                        f'{name}-site-content-{relative_key}',
                        bucket=bucket.bucket,
                        key=relative_key,
                        source=pulumi.asset.FileAsset(file_path),
                        content_type=content_type,
                        opts=ResourceOptions(parent=bucket)
                    )
                )

        # Set the access policy for the bucket so all objects are readable.
        s3.BucketPolicy(
            f'{name}-bucket-policy',
            bucket=bucket.bucket,
            policy=bucket.bucket.apply(_allow_getobject_policy),
            opts=ResourceOptions(parent=bucket))

        self.bucket = bucket
        self.website_url = bucket.website_endpoint

        self.register_outputs({
            'bucket': bucket,
            'websiteUrl': bucket.website_endpoint,
        })


def _allow_getobject_policy(bucket_name: str) -> str:
    return json.dumps({
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': [
                    f'arn:aws:s3:::{bucket_name}/*',  # policy refers to bucket name explicitly
                ],
            },
        ],
    })
