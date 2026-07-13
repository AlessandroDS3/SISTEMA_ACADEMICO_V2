"""Punto de entrada de la aplicacion Flask (Sistema Academico).

Uso:
    python run.py

El esquema de base de datos se gestiona con Flask-Migrate (Alembic),
NO con db.create_all(). Antes de correr la app por primera vez (o tras
cambiar un modelo), ejecutar:

    flask db upgrade      # aplica las migraciones pendientes en migrations/versions/

Si se modifica una entidad de dominio (nueva columna, nueva tabla, etc.):

    flask db migrate -m "Descripcion del cambio"
    flask db upgrade
"""
import os
from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "development"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
