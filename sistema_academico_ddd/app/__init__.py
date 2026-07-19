"""Application Factory del Sistema Academico.

Arquitectura en capas (Domain-Driven Design):
  - presentacion    -> Controllers (Flask Blueprints) + vistas
  - aplicacion      -> Application Services (orquestan casos de uso)
  - dominio         -> Entidades, Value Objects, Interfaces de Repositorio
  - infraestructura -> Implementaciones concretas (SQLAlchemy) y servicios externos
"""
import os
from flask import Flask

from config import config_by_name
from app.extensions import db, migrate


def create_app(config_name: str = None) -> Flask:
    """Crea y configura la instancia de la aplicacion Flask."""
    config_name = config_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder="presentacion/templates",
        static_folder="presentacion/static",
    )
    app.config.from_object(config_by_name[config_name])

    _inicializar_extensiones(app)
    _registrar_blueprints(app)

    return app


def _inicializar_extensiones(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)


def _registrar_blueprints(app: Flask) -> None:
    # Import local para evitar ciclos: los controllers usan `db`/modelos
    # que dependen de que las extensiones ya esten inicializadas.
    from app.presentacion.home_controller import home_bp
    from app.presentacion.usuario_controller import usuario_bp
    from app.presentacion.examen_controller import examen_bp
    from app.presentacion.respuesta_estudiante_controller import respuesta_estudiante_bp
    from app.presentacion.perfil_academico_controller import perfil_academico_bp
    from app.presentacion.reporte_institucional_controller import reporte_institucional_bp
    from app.presentacion.api_usuario_controller import api_usuario_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(usuario_bp, url_prefix="/usuarios")
    app.register_blueprint(examen_bp, url_prefix="/examenes")
    app.register_blueprint(respuesta_estudiante_bp, url_prefix="/respuestas")
    app.register_blueprint(perfil_academico_bp, url_prefix="/perfil-academico")
    app.register_blueprint(reporte_institucional_bp, url_prefix="/reportes")
    app.register_blueprint(api_usuario_bp, url_prefix="/api/usuarios")
