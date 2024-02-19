"""
run.py is the typical application server runner for flask.

Please note that this is only for a development server.
For production server, go for wsgi.py

"""

from aarc_apis import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000, host="localhost")
