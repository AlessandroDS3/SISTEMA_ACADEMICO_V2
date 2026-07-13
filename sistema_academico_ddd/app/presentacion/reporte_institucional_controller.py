"""Controller de presentacion: ReporteInstitucional (subdominio
Reportes_y_Estadisticas)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.contenedor import reporte_institucional_app_service, examen_app_service

reporte_institucional_bp = Blueprint("reporte_institucional", __name__)


@reporte_institucional_bp.route("/", methods=["GET"])
def listar():
    examen_id = request.args.get("examen_id", type=int)
    examenes = examen_app_service().listar_examenes()
    reportes = (
        reporte_institucional_app_service().listar_por_examen(examen_id) if examen_id else []
    )
    return render_template(
        "reportes/listar.html", reportes=reportes, examenes=examenes, examen_id=examen_id
    )


@reporte_institucional_bp.route("/generar", methods=["POST"])
def generar():
    examen_id = int(request.form["examen_id"])
    servicio = reporte_institucional_app_service()
    servicio.generar_reporte(examen_id)
    flash("Reporte institucional generado correctamente")
    return redirect(url_for("reporte_institucional.listar", examen_id=examen_id))
