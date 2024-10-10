from flask import Flask, session, render_template, request
import os
import logging
import colorama
from colorama import Fore, Style

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

first_time = True
first_time_panel = True
first_time_page = True

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
class bot():

    def page(name, template = None, **kwargs):
        @app.route(f"/{name}", endpoint=f"{name}_page")
        def create():
            """Creates a Page"""
            global first_time_page
            if first_time_page is True:
                print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f" Running the Bot With " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
                first_time_page = False
            if template is None:
                print(Fore.RED + "[ERROR]" + Fore.BLUE + " No Template Found" + Style.RESET_ALL)
            else:
                print(Fore.LIGHTMAGENTA_EX + "[LOG]" + Fore.BLUE + f" Page Loaded " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
                with app.app_context():
                    return render_template(template, **kwargs)

        return create()
    
    def panel(name, **kwargs):
        @staticmethod
        def decorator(func):
            @app.route(f"/{name}", methods=['GET', 'POST'], endpoint=f"{name}_page")
            def create():
                """Creates a Panel"""
                global first_time_panel
                if first_time_panel is True:
                    print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f" Running the Bot With " + Fore.YELLOW + name + Fore.BLUE + " directory" + Style.RESET_ALL)
                    first_time_panel = False
                else:
                    print(Fore.LIGHTMAGENTA_EX + "[LOG]" + Fore.BLUE + f" Page loaded " + Fore.YELLOW + name + Fore.BLUE + " directory" + Style.RESET_ALL)
                    data = request.args if request.method == 'GET' else request.form
                    return func()
                return func()
            return create
        return decorator

    @app.route("/")
    def home(template="index.html"):
        """Checks for the Template availability"""
        with app.app_context():
            global first_time
            if first_time is True:
                print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f" Running the Bot With " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
                first_time = False
            if not template:
                print(Fore.RED + "[ERROR]" + Fore.BLUE + " No Template Found" + Style.RESET_ALL)
                #template = "index.html"
                print(Fore.YELLOW + "[INFO]" + " " + Fore.BLUE + " Using default template" + Style.RESET_ALL)
                #app.run(port=port, debug=debug)
            else:
                print(Fore.LIGHTMAGENTA_EX + "[LOG]" + Fore.BLUE + f" Page loaded " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
                
                return render_template(template)
    

    @app.route("/")
    def run(port, debug = False):
        
        
        #if template is None:
            #template = "index.html"
            #print(Fore.YELLOW + "[INFO]" + Fore.BLUE + " Using default template" + Style.RESET_ALL)
            #app.run(port=port, debug=debug)
        #else:
            #print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f"Running the Bot With " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
        print(f"bot is running on http://localhost:{port}")
        app.run(port=port, debug=debug)
        print(f"bot is running on http://localhost:{port}")

