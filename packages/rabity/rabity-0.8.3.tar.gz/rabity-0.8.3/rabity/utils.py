import time
import base64
from flask import request, Flask, render_template, make_response
import os 
import zenora
from zenora import APIClient
from typing import Optional

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

class utils():
    class discord():
        def get_user_form_code(code, token, client_secret):
            client = APIClient(token, client_secret=client_secret)
            #accses_token = client.oauth.get_access_token(code, redirect_url).access_token
            user = client.users.get_current_user()
            return client.users.get_current_user()
    def wait(secs: int) -> None:
        """
        Pauses the program for a given number of seconds.
        
        :param secs: Number of seconds to wait
        """
        
        time.sleep(secs)
    def get_token_from_url(arg_name: Optional[str] = 'code') -> Optional[str]:
        """
        Retrieves a token or argument from the request URL.
        
        :param arg_name: Name of the argument to retrieve from the URL (default is 'code')
        :return: The value of the specified argument from the URL or None if not found
        """
        return request.args.get('code')
    def create_coockie(name: str, value: str):
        """
        Creates a cookie with the given name and value.
        
        :param name: Name of the cookie
        :param value: Value of the cookie
        """
        with app.app_context():
            response = make_response("Cookie has been set")
            response.set_cookie(name, value)
            return response
    def encrypt_in_base64(value: str):
        """
        encrypts the value to base64

        :param value: value to encrypt
        :return: encrypted value
        """
        return base64.b64encode(value.encode()).decode()
    def decrypt_from_base64(value: str):
        """
        decrypts the value from base64

        :param value: value to decrypt
        :return: decrypted value
        """
        return base64.b64decode(value.encode()).decode()
    def get_coockie(name: str):
        """
        Retrieves a cookie with the given name.
        
        :param name: Name of the cookie to retrieve
        :return: The value of the specified cookie or None if not found
        """
        return request.cookies.get(name)
    def get_html(path: str):
        """
        Loads the html file

        :param path: path for the html file
        :return: html file
        """
        with app.app_context():
            return render_template(path)



