release: export FLASK_APP=flasksite
release: flask init-db
web: waitress-serve --call flasksite:create_app