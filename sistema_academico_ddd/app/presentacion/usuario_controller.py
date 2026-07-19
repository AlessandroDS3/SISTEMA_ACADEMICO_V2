"""Controller de presentacion: Usuario (subdominio Autenticacion_y_Usuarios).

Expone las operaciones del `UsuarioAppService` como rutas web (MVC).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.contenedor import usuario_app_service
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.presentacion.decoradores import manejar_errores_de_dominio

usuario_bp = Blueprint("usuario", __name__)


def _ir_al_listado(*_args, **_kwargs):
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/", methods=["GET"])
def listar():
    servicio = usuario_app_service()
    usuarios = servicio.listar_usuarios()
    return render_template("usuarios/listar.html", usuarios=usuarios, roles=RolEnum)


@usuario_bp.route("/nuevo", methods=["POST"])
@manejar_errores_de_dominio(_ir_al_listado)
def crear():
    servicio = usuario_app_service()
    servicio.registrar_usuario(
        username=request.form["username"],
        password=request.form["password"],
        rol=RolEnum(request.form.get("rol", RolEnum.ESTUDIANTE.value)),
    )
    flash("Usuario creado correctamente")
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/<int:usuario_id>/editar", methods=["GET"])
def editar(usuario_id: int):
    servicio = usuario_app_service()
    usuario = servicio.obtener_por_id(usuario_id)
    if usuario is None:
        flash("Usuario no encontrado")
        return redirect(url_for("usuario.listar"))
    return render_template("usuarios/editar.html", usuario=usuario, roles=RolEnum)


@usuario_bp.route("/<int:usuario_id>/editar", methods=["POST"])
@manejar_errores_de_dominio(_ir_al_listado)
def actualizar(usuario_id: int):
    servicio = usuario_app_service()
    servicio.actualizar_usuario(
        usuario_id=usuario_id,
        username=request.form["username"],
        rol=RolEnum(request.form.get("rol", RolEnum.ESTUDIANTE.value)),
        password=request.form.get("password") or None,
    )
    flash("Usuario actualizado correctamente")
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/<int:usuario_id>/eliminar", methods=["POST"])
def eliminar(usuario_id: int):
    servicio = usuario_app_service()
    servicio.eliminar_usuario(usuario_id)
    return redirect(url_for("usuario.listar"))
