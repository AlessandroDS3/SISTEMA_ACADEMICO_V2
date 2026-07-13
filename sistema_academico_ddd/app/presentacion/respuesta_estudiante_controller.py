"""Controller de presentacion: RespuestaEstudiante (subdominio
Calificacion_Automatica). Permite subir la imagen escaneada de una
hoja de examen y calificarla automaticamente (OMR)."""
import os
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from app.contenedor import respuesta_estudiante_app_service, examen_app_service
from app.extensions import db
from app.dominio.autenticacion_usuarios.usuario import Usuario

respuesta_estudiante_bp = Blueprint("respuesta_estudiante", __name__)


@respuesta_estudiante_bp.route("/", methods=["GET"])
def listar():
    servicio = respuesta_estudiante_app_service()
    examen_id = request.args.get("examen_id", type=int)
    respuestas = servicio.listar_por_examen(examen_id) if examen_id else []
    examenes = examen_app_service().listar_examenes()
    estudiantes = db.session.query(Usuario).all()
    return render_template(
        "respuestas/listar.html",
        respuestas=respuestas,
        examenes=examenes,
        estudiantes=estudiantes,
        examen_id=examen_id,
    )


@respuesta_estudiante_bp.route("/procesar", methods=["POST"])
def procesar():
    archivo = request.files.get("imagen")
    examen_id = int(request.form["examen_id"])
    estudiante_id = int(request.form["estudiante_id"])

    if not archivo or archivo.filename == "":
        flash("Debes seleccionar una imagen de la hoja escaneada")
        return redirect(url_for("respuesta_estudiante.listar", examen_id=examen_id))

    carpeta_subidas = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(carpeta_subidas, exist_ok=True)
    nombre_archivo = f"{uuid.uuid4().hex}_{archivo.filename}"
    ruta_imagen = os.path.join(carpeta_subidas, nombre_archivo)
    archivo.save(ruta_imagen)

    servicio = respuesta_estudiante_app_service()
    try:
        servicio.procesar_hoja_escaneada(examen_id, estudiante_id, ruta_imagen)
        flash("Hoja de examen procesada y calificada correctamente")
    except Exception as error:  # noqa: BLE001 - mostramos el error al usuario
        flash(f"No se pudo procesar la imagen: {error}")

    return redirect(url_for("respuesta_estudiante.listar", examen_id=examen_id))
