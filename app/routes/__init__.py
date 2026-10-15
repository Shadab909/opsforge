from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.modules import modules_bp
from app.routes.quiz import quiz_bp
from app.routes.progress import progress_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
