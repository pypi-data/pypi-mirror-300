from pathlib import Path
from uuid import uuid4

import boto3
from moto import mock_aws

from pys3thon.client import S3Client


@mock_aws
def test_upload_file(tmpdir):
    tmpdir = Path(tmpdir)
    conn = boto3.resource("s3", region_name="ap-southeast-2")
    conn.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )
    s3_client = S3Client()
    source_bucket = "test-bucket"
    source_key = f"{str(uuid4())}/Nepean.pdf"

    tmp_file_path = str(tmpdir / "Nepean.pdf")
    with open(tmp_file_path, "w") as file1:
        # Write some content to the file
        file1.write("Hello, world!")

    s3_client.upload_file(tmp_file_path, source_bucket, source_key)
    assert s3_client.check_if_exists_in_s3(source_bucket, source_key)


@mock_aws
def test_upload_file_with_key_that_is_uri_encoded(tmpdir):
    tmpdir = Path(tmpdir)
    conn = boto3.resource("s3", region_name="ap-southeast-2")
    conn.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )
    s3_client = S3Client()
    source_bucket = "test-bucket"
    source_key = f"{str(uuid4())}/Nepean%20Legend(2).pdf"

    tmp_file_path = str(tmpdir / "Nepean.pdf")
    with open(tmp_file_path, "w") as file1:
        # Write some content to the file
        file1.write("Hello, world!")

    s3_client.upload_file(tmp_file_path, source_bucket, source_key)
    assert s3_client.check_if_exists_in_s3(source_bucket, source_key)


@mock_aws
def test_upload_file_with_key_that_is_not_uri_encoded_with_spaces(tmpdir):
    tmpdir = Path(tmpdir)
    conn = boto3.resource("s3", region_name="ap-southeast-2")
    conn.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "ap-southeast-2"},
    )
    s3_client = S3Client()
    source_bucket = "test-bucket"
    source_key = f"{str(uuid4())}/Nepean Legend(2).pdf"

    tmp_file_path = str(tmpdir / "Nepean.pdf")
    with open(tmp_file_path, "w") as file1:
        # Write some content to the file``
        file1.write("Hello, world!")

    s3_client.upload_file(tmp_file_path, source_bucket, source_key)
    assert s3_client.check_if_exists_in_s3(source_bucket, source_key)
