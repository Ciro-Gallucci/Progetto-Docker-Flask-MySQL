from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_view = 'auth.login'

    migrate = Migrate(app, db)

    from app import models
    from app.models import User  # Assumendo che il modello User esista!

    # Route principale per vedere tutti gli utenti
    @app.route('/')
    def list_users():
        users = User.query.all()
        user_list = '<br>'.join([f"ID: {user.id}, Username: {user.username}" for user in users])
        return (
            "<h1>Lista Utenti</h1>"
            f"{user_list if user_list else 'Nessun utente trovato.'}"
            "<br><br>"
            '<a href="' + url_for('add_user') + '">Aggiungi nuovo utente</a>'
        )

    # Route per aggiungere un utente
    @app.route('/add', methods=['GET', 'POST'])
    def add_user():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            if not username or not email:
                return 'Devi specificare username ed email!', 400

            # Crea un nuovo utente
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('list_users'))

        # Form HTML per l'aggiunta
        return (
            "<h1>Aggiungi Nuovo Utente</h1>"
            "<form method='post'>"
            "Username: <input type='text' name='username'><br>"
            "Email: <input type='email' name='email'><br>"
            "<input type='submit' value='Aggiungi'>"
            "</form>"
            "<br>"
            "<a href='/'>Torna alla lista</a>"
        )

    return app
