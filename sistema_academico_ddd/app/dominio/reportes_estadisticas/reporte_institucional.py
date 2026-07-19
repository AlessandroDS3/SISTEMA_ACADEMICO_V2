"""Entidad de dominio ReporteInstitucional (raiz de agregado del
subdominio Reportes_y_Estadisticas)."""

from app.dominio.tiempo import ahora_utc
from app.extensions import db
from app.dominio.reportes_estadisticas.estadistica_grupal import EstadisticaGrupal


class ReporteInstitucional(db.Model):
    __tablename__ = "reportes_institucionales"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    generado_en = db.Column(db.DateTime, default=ahora_utc)
    promedio_general = db.Column(db.Float, nullable=False, default=0.0)
    desviacion_estandar = db.Column(db.Float, nullable=False, default=0.0)

    estadisticas_grupales = db.relationship(
        "EstadisticaGrupal", back_populates="reporte", cascade="all, delete-orphan"
    )
    examen = db.relationship("Examen")

    def registrar_estadistica_grupo(
        self,
        asignacion_grupo_id: int,
        promedio_grupo: float,
        numero_aprobados: int,
        numero_desaprobados: int,
    ) -> EstadisticaGrupal:
        """Estilo Things: el ReporteInstitucional (raiz de agregado) es
        quien crea y enlaza sus propias EstadisticaGrupal, en vez de
        que la capa de aplicacion construya el hijo a mano y lo agregue
        a la sesion de SQLAlchemy por su cuenta."""
        estadistica = EstadisticaGrupal(
            asignacion_grupo_id=asignacion_grupo_id,
            promedio_grupo=promedio_grupo,
            numero_aprobados=numero_aprobados,
            numero_desaprobados=numero_desaprobados,
        )
        estadistica.reporte = self
        self.estadisticas_grupales.append(estadistica)
        return estadistica
