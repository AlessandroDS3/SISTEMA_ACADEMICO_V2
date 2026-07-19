"""Controller de presentacion: PerfilAcademico (subdominio
Seguimiento_Academico)."""
from typing import Dict

from flask import Blueprint, render_template

from app.contenedor import perfil_academico_app_service, usuario_app_service

perfil_academico_bp = Blueprint("perfil_academico", __name__)


@perfil_academico_bp.route("/", methods=["GET"])
def listar():
    perfiles = perfil_academico_app_service().listar_perfiles()
    return render_template(
        "perfil_academico/listar.html",
        perfiles=perfiles,
        estudiantes=_nombres_de_estudiantes(),
    )


def _nombres_de_estudiantes() -> Dict[int, str]:
    """Devuelve un mapa `id -> username` pidiendoselo al servicio de usuarios.

    Practica Clean Code (Objetos y Estructuras de Datos / Ley de Demeter):
    la capa de presentacion ya no habla con SQLAlchemy ni conoce la
    entidad `Usuario`; solo llama al servicio de aplicacion que le
    corresponde.
    """
    usuarios = usuario_app_service().listar_usuarios()
    return {usuario.id: usuario.username for usuario in usuarios}
