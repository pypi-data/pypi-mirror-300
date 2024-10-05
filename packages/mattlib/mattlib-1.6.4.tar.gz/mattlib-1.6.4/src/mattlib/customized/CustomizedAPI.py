import sys
sys.path.append('../mattlib')
from mattlib.BaseAPI import BaseAPI
import requests
import json

class CustomizedAPI(BaseAPI):
    required_info = [
    ]

    def __init__(self, name, methods):
        self.name=name
        self._methods = methods
        
    def connect(self, body: dict, url_connection: str= None, url_variables: dict = None):
        self.headers = None
        self.auth = None
        if url_connection==None:
            self.auth=requests.auth.HTTPBasicAuth(*body.values())
        else:
            self.url_connection = url_connection.format(**url_variables)
            self.__get_auth_user(body)

    def __get_auth_user(self, params):
        response = requests.post(self.url_connection, data=params)
        token = response.json().get('access_token')
        if token != None:
            self.headers = {'Authorization': f'Bearer {token}'}
            return 
        else:
            raise Exception(f"{self.name} authentication failed.\n "\
                  f"Response: {response}")
        
    def generic_method(self, url_method: str, url_variables: dict, format: str, next_link: json = {'key': '', 'key_give_complete_url': False}, key_response: str = ''):
        url_method_call = url_method.format(**url_variables)
        if format == 'csv':
            response = self.call_api_stream(url_method_call)
        elif format == 'json':
            response = self.call_api(url_method_call, next_link, key_response)
        return response
        
    def call_api_stream(self, url_method_call):
        if(self.headers!=None):
            response = requests.get(url_method_call, headers=self.headers)
        elif(self.auth!=None):
            response = requests.get(url_method_call, auth=self.auth)
        return response.text

    def call_api(self, url_method_call, next_link, key_response):
        values = []
        url = url_method_call
        while url != None:
            if(self.headers!=None):
                response = requests.get(url_method_call, headers=self.headers)
            elif(self.auth!=None):
                response = requests.get(url_method_call, auth=self.auth)
            status = response.status_code 

            if status != 200:
                return None
            
            response = json.loads(response.text)
            
            if key_response =='':
                return response

            values += response[key_response]
            if next_link['key'] in response.keys():
                if next_link['key_give_complete_url']:
                    url = response[next_link['key']]
                else:
                    url = url_method_call + response[next_link['key']]
            else :
                url = None
        return values
    
    def methods(self):
        return self._methods