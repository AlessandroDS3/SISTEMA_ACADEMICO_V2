"""Controller de presentacion: PerfilAcademico (subdominio
Seguimiento_Academico)."""
from flask import Blueprint, render_template

from app.contenedor import perfil_academico_app_service
from app.extensions import db
from app.dominio.autenticacion_usuarios.usuario import Usuario

perfil_academico_bp = Blueprint("perfil_academico", __name__)


@perfil_academico_bp.route("/", methods=["GET"])
def listar():
    servicio = perfil_academico_app_service()
    perfiles = servicio.listar_perfiles()
    estudiantes = {u.id: u.username for u in db.session.query(Usuario).all()}
    return render_template("perfil_academico/listar.html", perfiles=perfiles, estudiantes=estudiantes)
