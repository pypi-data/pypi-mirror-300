import time
from flask import request, Flask, render_template, make_response
import os 
from typing import Optional

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

class utils():
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
        
    def get_coockie(name: str):
        """
        Retrieves a cookie with the given name.
        
        :param name: Name of the cookie to retrieve
        :return: The value of the specified cookie or None if not found
        """
        return request.cookies.get(name)