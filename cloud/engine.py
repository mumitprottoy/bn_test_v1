import boto3
from ._cloud_creds import cloud_cred
from utils.keygen import KeyGen
from django.core.files.uploadedfile import UploadedFile


class CloudEngine:

    def __init__(
            self,
            file: UploadedFile,  
            bucket: str='testv0', 
            key_holder: str='mumit1', 
            region: str='auto',
            file_name_header_len: int=10) -> None:
        
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
    
    @property
    def client(self):
        return boto3.client(
            service_name=self.service_name,
            region_name=self.region,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def __set_file_name(self, original_file_name: str) -> str:
        ext = original_file_name.split('.')[-1].lower()
        name = KeyGen().timestamped_alphanumeric_id(
            head_len=self.file_name_header_len)
        return f'{name}.{ext}'
    
    def __get_file_public_url(self, cloud_file_name: str) -> str:
        return f'{self.public_base_url}/{cloud_file_name}'
    
    def upload(self) -> str | None:
        print(self.__dict__)
        cloud_file_name = self.__set_file_name(self.file.name)
        try:
            response = self.client.upload_fileobj(
                self.file.file, self.bucket, cloud_file_name)
            print(response)
            return self.__get_file_public_url(cloud_file_name)
        except Exception as e:
            self.errors.append(str(e))
