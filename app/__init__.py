import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)

    # Trust one proxy hop from cloudflared/Cloudflare.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Browsers cache static files for hours, so after a deploy a fresh page
    # could pair with a stale style.css/main.js. Tagging each static URL with
    # the file's modified time gives it a new URL whenever the file changes.
    @app.url_defaults
    def version_static_urls(endpoint, values):
        if endpoint != "static" or "filename" not in values:
            return
        path = os.path.join(app.static_folder, values["filename"])
        if os.path.isfile(path):
            values["v"] = int(os.path.getmtime(path))

    from .routes import bp
    app.register_blueprint(bp)

    return app

