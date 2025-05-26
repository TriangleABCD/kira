from openai import OpenAI
from kira_utils import get_api_key, get_encrypted_api_key, multi_line_input

class Model:
    def __init__(self, vendor_name='', url='', v3='', r1='', key_path='', key_key_path='', encrypt=False):
        self.vendor_name = vendor_name
        self.url = url
        self.model_v3_name = v3
        self.model_r1_name = r1

        self.api_key_path = key_path
        self.api_key_key_path = key_key_path
        self.api_key_encrypt = encrypt

        self.client = None
        self.init_client(self)

        self.message = [{
            "role": "system",
            "content": "你是领域专家，从专业角度回答用户问题，优先考虑专业性"
        }]

    def init_client(self):
        api_key = None
        if self.api_key_encrypt:
            api_key = get_encrypted_api_key(self.api_key_path, self.api_key_key_path)
        else:
            api_key = get_api_key(self.api_key_path)

        self.client =  OpenAI(
            api_key = api_key,
            base_url = self.url
        )


    def chat_once(self):
        pass


    def chat(self):
        pass
