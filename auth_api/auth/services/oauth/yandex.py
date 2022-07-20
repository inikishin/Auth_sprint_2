import os
import requests


class YandexOAuthService:
    def __init__(self):
        self.client_id = os.getenv('OAUTH_YANDEX_CLIENT_ID')
        self.client_secret = os.getenv('OAUTH_YANDEX_CLIENT_SECRET')
        self.oauth_url = 'https://oauth.yandex.ru/'
        self.login_url = 'https://login.yandex.ru/'

    def get_authorize_url(self, state: str = None) -> str:
        """Формирование адреса для авторизации в яндексе"""
        authorize_url = self.oauth_url + 'authorize?'
        authorize_url = authorize_url + 'response_type=code'
        authorize_url = authorize_url + f'&client_id={self.client_id}'

        if state:
            authorize_url = authorize_url + f'&state={state}'

        return authorize_url


    def get_token(self, confirmation_code: str, state: str = None):
        """Обмен кода подтверждения на токен."""
        url = self.oauth_url + 'token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'authorization_code',
            'code': confirmation_code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        request = requests.post(url, data=payload, headers=headers)
        data = None

        if request.status_code == 400:
            data = request.json()
            data['authorize_url'] = self.get_authorize_url()

        if request.status_code == 200:
            data = request.json()

        return data

    def refresh_token(self, refresh_token):
        """Обновление токена через refresh_token."""
        url = self.oauth_url + 'token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        request = requests.post(url, data=payload, headers=headers)
        data = None

        if request.status_code == 400:
            data = request.json()

        if request.status_code == 200:
            data = request.json()

        return data

    def get_user_info(self, access_token):
        """Запрос информации о пользователе."""
        url = self.login_url + 'info'
        headers = {
            'Authorization': f'OAuth {access_token}',
        }
        request = requests.get(url, headers=headers)

        data = None

        if request.status_code == 400:
            data = request.json()

        if request.status_code == 200:
            data = request.json()

        return data
