import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

google_api_base_dir = os.getcwd()


class GoogleBaseAPI:

    def __init__(self, email, tokens_dirname):
        self.req_email = email
        self.credentials = None
        self.__userinfo_service = None
        self.__email = None
        self.scopes_base = ['https://www.googleapis.com/auth/userinfo.email']
        self.tokens_dirname = tokens_dirname

    @property
    def userinfo_service(self):
        if self.__userinfo_service is None:
            self.__userinfo_service = build('oauth2', 'v2', credentials=self.credentials)

        return self.__userinfo_service

    @property
    def email(self):
        if self.__email is None:
            self.__email = self.userinfo_service.userinfo().get().execute()['email']
        return self.__email

    def auth(self, scopes):
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

        scopes.extend(self.scopes_base)
        tokens_path = os.path.join(google_api_base_dir, f'{self.tokens_dirname}/{self.req_email}.json')

        desktop_credentials_path = os.path.join(google_api_base_dir, 'config', 'desktop_credentials.json')

        self.credentials = None
        # if token already exists
        if os.path.exists(tokens_path):
            self.credentials = Credentials.from_authorized_user_file(tokens_path, scopes)

        # if not exists or invalid
        if not self.credentials or not self.credentials.valid:
            # init auth flow
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(desktop_credentials_path, scopes)
                self.credentials = flow.run_local_server(port=0)

        if self.req_email != self.email:

            if os.path.exists(tokens_path):
                # clear the tokens since they most likely tinkered with
                os.remove(tokens_path)

            raise Exception(
                f'Requested email [{self.req_email}] does not match authenticated email [{self.email}].')
        else:
            tokens_path = os.path.join(google_api_base_dir, f'{self.tokens_dirname}/{self.email}.json')
            os.makedirs(os.path.dirname(tokens_path), exist_ok=True)
            with open(tokens_path, 'w') as token:
                token.write(self.credentials.to_json())
