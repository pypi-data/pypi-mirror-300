from flask import Flask, session, render_template
import RunwayLib
import os
import colorama
from colorama import Fore, Style

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
class bot():

    def page(name):
        @app.route(f"/{name}")
        def create(template = None):
            """Creates a Page"""
            if template is None:
                print(Fore.RED + "[ERROR]" + Fore.BLUE + " No Template Found" + Style.RESET_ALL)
            else:
                print(print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f"Running the Bot With " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL))
                return render_template(template)
        return create
    @app.route("/")
    def home(template="index.html"):
        """Checks for the Template availability"""
        with app.app_context():
            if not template:
                print(Fore.RED + "[ERROR]" + Fore.BLUE + " No Template Found" + Style.RESET_ALL)
                #template = "index.html"
                print(Fore.YELLOW + "[INFO]" + Fore.BLUE + " Using default template" + Style.RESET_ALL)
                #app.run(port=port, debug=debug)
            else:
                print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f"Running the Bot With " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
                return render_template(template)
    

    @app.route("/")
    def run(token, port, template = None, debug = False):
        
        
        #if template is None:
            #template = "index.html"
            #print(Fore.YELLOW + "[INFO]" + Fore.BLUE + " Using default template" + Style.RESET_ALL)
            #app.run(port=port, debug=debug)
        #else:
            #print(Fore.YELLOW + "[INFO]" + Fore.BLUE + f"Running the Bot With " + Fore.YELLOW + template + Fore.BLUE + " directory" + Style.RESET_ALL)
        app.run(port=port, debug=debug)
        print(f"bot is running on http://localhost:{port}")
