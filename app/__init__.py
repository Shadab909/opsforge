from flask import Flask, session, render_template
from app.config import Config
from app.database import get_profile, list_profiles
from app.routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Context processor to inject active profile and metadata into all templates
    @app.context_processor
    def inject_global_data():
        username = session.get("username")
        current_user = get_profile(username) if username else None
        profiles = list_profiles()
        return {
            "current_user": current_user,
            "available_profiles": profiles,
            "app_name": "OpsForge"
        }

    # Fallback asset route
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        from flask import send_from_directory
        return send_from_directory(Config.BASE_DIR / 'app' / 'static' / 'assets', filename)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Register blueprints
    register_blueprints(app)

    return app
