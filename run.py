from flaskr import create_app
from flaskr.db import init_db

if __name__ == "__main__":
    #le mode debug permet d'avoir une page avec les messages d'erreurs
    create_app().run(debug=True)