import boto3
from ._cloud_creds import cloud_cred
from utils import keygen as kg, constants as const
from django.core.files.uploadedfile import UploadedFile
from botocore.client import Config


class CloudEngine:

    def __init__(
            self,
            file: UploadedFile=None,  
            bucket: str='testv0', 
            key_holder: str='mumit1', 
            region: str='auto',
            file_name_header_len: int=10) -> None:
        
        self.bucket_code = bucket
        self.file = file
        self.creds = cloud_cred
        self.service_name = self.creds.service_name
        self.bucket = self.creds.bucket.__dict__[bucket]
        self.region = self.creds.region.__dict__[region]
        self.access_key = self.creds.access_key.__dict__[key_holder]
        self.secret_key = self.creds.secret_key
        self.endpoint_url = self.creds.get_endpoint_url()
        self.public_base_url = self.creds.public_base_urls[bucket]
        self.file_name_header_len = file_name_header_len
        self.errors = list()
    
    def get_file_upload_key(self, file_name: str) -> str | None:
        ext = file_name.lower().split('.')[-1]
        if ext in const.BUCKET_EXT_MAP[self.bucket_code]:
            return kg.KeyGen().timestamped_alphanumeric_id() + '.' + ext
        else: self.errors.append(f'Bucket: {self.bucket_code} does not support file-type: {ext}')
 
    @property
    def client(self):
        return boto3.client(
            service_name=self.service_name,
            region_name=self.region,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4')
        )

    def __set_file_name(self, original_file_name: str) -> str:
        ext = original_file_name.split('.')[-1].lower()
        name = kg.KeyGen().timestamped_alphanumeric_id(
            head_len=self.file_name_header_len)
        return f'{name}.{ext}'
    
    def __get_file_public_url(self, cloud_file_name: str) -> str:
        return f'{self.public_base_url}/{cloud_file_name}'
    
    def upload(self) -> str | None:
        cloud_file_name = self.__set_file_name(self.file.name)
        try:
            response = self.client.upload_fileobj(
                self.file.file, self.bucket, cloud_file_name)
            print(response)
            return self.__get_file_public_url(cloud_file_name)
        except Exception as e:
            self.errors.append(str(e))
    
    def initiate_multipart_upload(self, key: str) -> str | None:
        try:
            resp = self.client.create_multipart_upload(
                Bucket=self.bucket,
                Key=key
            )
            return resp["UploadId"]
        except Exception as e:
            self.errors.append(str(e))
            return None

    def get_presigned_url_for_part_upload(
            self, key: str, upload_id: str, part_number: int, expires=3600) -> str | None:
        try:
            return self.client.generate_presigned_url(
                ClientMethod="upload_part",
                Params={
                    "Bucket": self.bucket,
                    "Key": key,
                    "UploadId": upload_id,
                    "PartNumber": part_number
                },
                ExpiresIn=expires
            )
        except Exception as e:
            self.errors.append(str(e))
            return None

    def complete_multipart_upload(self, key: str, upload_id: str, parts: list[dict]) -> dict | None:
        """
        parts must be a list of dicts:
        [{"PartNumber": int, "ETag": str}, ...]
        """
        try:
            resp = self.client.complete_multipart_upload(
                Bucket=self.bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts}
            )
            return resp
        except Exception as e:
            self.errors.append(str(e))
            return None

    def abort_multipart_upload(self, key: str, upload_id: str) -> dict | None:
        try:
            resp = self.client.abort_multipart_upload(
                Bucket=self.bucket,
                Key=key,
                UploadId=upload_id
            )
            return resp
        except Exception as e:
            self.errors.append(str(e))
