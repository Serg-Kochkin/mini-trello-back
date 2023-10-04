from app import flask_app
import app.routes

if __name__ == "__main__":
    """Run server"""
    import os

    os.environ['FLASK_APP'] = 'app'

    flask_app.run(host='0.0.0.0', port=5000)
