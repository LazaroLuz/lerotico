from flask import Flask
# from pyngrok import conf, ngrok
from core.view import views
import os


app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')

if __name__ == '__main__':
    # os.system('loophole http 5000 --hostname lerotics')
    # os.system('loophole dir Donwload --hostname fotosvideos')
    app.run(debug=True)
