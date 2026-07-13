"""Extensiones de Flask compartidas por toda la aplicacion.

Se instancian aqui (sin `app`) para evitar import circular; se
enlazan a la app real dentro de `create_app()` (Application Factory).
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
