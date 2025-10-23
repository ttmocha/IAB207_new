from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Where to store uploaded images (relative to your package)
    # The files will end up in <yourpkg>/static/image/uploads
    app.config['UPLOAD_FOLDER'] = 'static/image/uploads'

    db.init_app(app)
    Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User  # ensure models are registered

    @login_manager.user_loader
    def load_user(user_id):
        # cast to int when PK is integer; return None on bad input
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    # Blueprints
    from .views import main_bp
    app.register_blueprint(main_bp)

    try:
        from .auth import auth_bp
        app.register_blueprint(auth_bp)
    except Exception:
        pass

    # Dev/assignment convenience: create tables if not exist
    with app.app_context():
        db.create_all()

    return app
