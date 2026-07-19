"""Controller de presentacion: Examen (subdominio Gestion_de_Examenes)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.contenedor import examen_app_service
from app.extensions import db
from app.dominio.area_materia.materia import Materia
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.presentacion.decoradores import manejar_errores_de_dominio

examen_bp = Blueprint("examen", __name__)


def _ir_al_listado(*_args, **_kwargs):
    return redirect(url_for("examen.listar"))


@examen_bp.route("/", methods=["GET"])
def listar():
    servicio = examen_app_service()
    examenes = servicio.listar_examenes()
    materias = db.session.query(Materia).all()
    docentes = db.session.query(Usuario).all()
    return render_template(
        "examenes/listar.html", examenes=examenes, materias=materias, docentes=docentes
    )


@examen_bp.route("/nuevo", methods=["POST"])
def crear():
    servicio = examen_app_service()
    servicio.crear_examen(
        titulo=request.form["titulo"],
        materia_id=int(request.form["materia_id"]),
        creado_por_id=int(request.form["creado_por_id"]),
        numero_preguntas=int(request.form["numero_preguntas"]),
        numero_alternativas=int(request.form.get("numero_alternativas", 4)),
        puntaje_por_pregunta=float(request.form.get("puntaje_por_pregunta", 1.0)),
    )
    flash("Examen creado correctamente")
    return redirect(url_for("examen.listar"))


@examen_bp.route("/<int:examen_id>/editar", methods=["GET"])
def editar(examen_id: int):
    servicio = examen_app_service()
    examen = servicio.obtener_por_id(examen_id)
    if examen is None:
        flash("Examen no encontrado")
        return redirect(url_for("examen.listar"))
    materias = db.session.query(Materia).all()
    return render_template("examenes/editar.html", examen=examen, materias=materias)


@examen_bp.route("/<int:examen_id>/editar", methods=["POST"])
@manejar_errores_de_dominio(_ir_al_listado)
def actualizar(examen_id: int):
    servicio = examen_app_service()
    servicio.actualizar_examen(
        examen_id=examen_id,
        titulo=request.form["titulo"],
        materia_id=int(request.form["materia_id"]),
        numero_preguntas=int(request.form["numero_preguntas"]),
        numero_alternativas=int(request.form.get("numero_alternativas", 4)),
        puntaje_por_pregunta=float(request.form.get("puntaje_por_pregunta", 1.0)),
    )
    flash("Examen actualizado correctamente")
    return redirect(url_for("examen.listar"))


@examen_bp.route("/<int:examen_id>/eliminar", methods=["POST"])
def eliminar(examen_id: int):
    servicio = examen_app_service()
    servicio.eliminar_examen(examen_id)
    return redirect(url_for("examen.listar"))
