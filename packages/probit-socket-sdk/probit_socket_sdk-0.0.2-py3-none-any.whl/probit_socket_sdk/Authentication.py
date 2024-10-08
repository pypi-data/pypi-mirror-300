import base64
import requests
import json


class Authentication:
    __apiClientId: str
    __apiClientSecret: str
    __token: str

    def __init__(self, api_client_id, api_client_secret):
        self.__apiClientId = api_client_id
        self.__apiClientSecret = api_client_secret
        self.__generate_token()

    def get_token(self):
        return self.__token

    def __get_bearer_token(self):
        concatenated_credentials = f"{self.__apiClientId}:{self.__apiClientSecret}"
        encoded_base64 = base64.b64encode(concatenated_credentials.encode()).decode()
        auth_header = f"Basic {encoded_base64}"
        return auth_header

    def __generate_token(self):
        try:
            auth_header = self.__get_bearer_token()
            payload = {"grant_type": "client_credentials"}
            url = "https://accounts.probit.com/token"

            headers = {
                "accept": "application/json",
                "Authorization": auth_header,
                "content-type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)

            if not response.ok:
                raise RuntimeError(f"Authentication Required - {response.status_code} : {response.reason}")

            self.__token = json.loads(response.text)['access_token']
        except Exception as inst:
            print(inst)
            exit(0)
