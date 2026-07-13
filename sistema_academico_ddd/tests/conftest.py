"""Fixtures compartidos para las pruebas del Sistema Academico.

Usamos una base de datos SQLite temporal (archivo, no ':memory:') para
que la conexion se comparta correctamente entre requests dentro de un
mismo test, y la destruimos al terminar cada test para que las pruebas
no interfieran entre si.
"""
import os
import tempfile

import pytest

from app import create_app
from app.extensions import db as _db


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    flask_app = create_app("testing")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db
