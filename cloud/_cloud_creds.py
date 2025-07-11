service_name = 's3'
public_base_url = 'https://pub-2def41345f13434aa37c16ee78e1fbcc.r2.dev'
account_id = 'bdf1650e0f6d38c742f87b7703a2e2d4'
secret_key = '7dd3b2e08fbbda9a627ed1455dbe3f79047ed697d17394110c924f0617bbf2a6'
api_tokens = {
    'mumit1': 'SO64L5Lz_zYjm3zQy0kZetyXF4QNWq6O8ssipsw_'
}
access_keys = {
    'mumit1': 'cef3a724a56beacceed51c2d06c7c60b'
}
buckets = {
    'testv0': 'bwlrntktestv0',
    'testv1': 'bwlrntktestv1',
    'testv2': 'bwlrntktestv2'
}
regions = {
    'auto': 'auto'
}

class DictData:
    
    def __init__(self, **kwargs) -> None:
        for k,v in kwargs.items():
            self.__dict__[k] = v


class CloudCred:

    def __init__(self) -> None:
        self.service_name = service_name
        self.account_id = account_id
        self.secret_key = secret_key
        self.access_key = DictData(**access_keys)
        self.bucket = DictData(**buckets)
        self.region = DictData(**regions)
        self.public_base_url = public_base_url
    
    def get_endpoint_url(self) -> str:
        return f'https://{self.account_id}.r2.cloudflarestorage.com'


cloud_cred = CloudCred()