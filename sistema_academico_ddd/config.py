"""Configuracion de la aplicacion Flask (Sistema Academico).

Sigue el patron estandar de Flask: una clase base `Config` y
subclases por entorno (Development, Testing, Production).
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-dev-cambiar-en-produccion")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'sistema_academico.db')}"
    )
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
