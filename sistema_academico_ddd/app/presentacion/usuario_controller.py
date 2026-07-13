"""Controller de presentacion: Usuario (subdominio Autenticacion_y_Usuarios).

Expone las operaciones del `UsuarioAppService` como rutas web (MVC).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.contenedor import usuario_app_service
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum

usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.route("/", methods=["GET"])
def listar():
    servicio = usuario_app_service()
    usuarios = servicio.listar_usuarios()
    return render_template("usuarios/listar.html", usuarios=usuarios, roles=RolEnum)


@usuario_bp.route("/nuevo", methods=["POST"])
def crear():
    servicio = usuario_app_service()
    try:
        servicio.registrar_usuario(
            username=request.form["username"],
            password=request.form["password"],
            rol=RolEnum(request.form.get("rol", RolEnum.ESTUDIANTE.value)),
        )
        flash("Usuario creado correctamente")
    except ValueError as error:
        flash(str(error))
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/<int:id>/editar", methods=["GET"])
def editar(id: int):
    servicio = usuario_app_service()
    usuario = servicio.obtener_por_id(id)
    if usuario is None:
        flash("Usuario no encontrado")
        return redirect(url_for("usuario.listar"))
    return render_template("usuarios/editar.html", usuario=usuario, roles=RolEnum)


@usuario_bp.route("/<int:id>/editar", methods=["POST"])
def actualizar(id: int):
    servicio = usuario_app_service()
    try:
        servicio.actualizar_usuario(
            id=id,
            username=request.form["username"],
            rol=RolEnum(request.form.get("rol", RolEnum.ESTUDIANTE.value)),
            password=request.form.get("password") or None,
        )
        flash("Usuario actualizado correctamente")
    except ValueError as error:
        flash(str(error))
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id: int):
    servicio = usuario_app_service()
    servicio.eliminar_usuario(id)
    return redirect(url_for("usuario.listar"))
