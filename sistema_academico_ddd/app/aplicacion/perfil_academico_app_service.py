"""Application Service: casos de uso de Seguimiento_Academico (consultar
y actualizar el perfil academico consolidado de un estudiante)."""
from typing import List, Optional

from app.extensions import db
from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico
from app.dominio.seguimiento_academico.perfil_academico_repositorio import (
    IPerfilAcademicoRepositorio,
)
from app.dominio.seguimiento_academico.evolucion_nota import EvolucionNota
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)


class PerfilAcademicoAppService:

    def __init__(
        self,
        perfil_repositorio: IPerfilAcademicoRepositorio,
        respuesta_repositorio: IRespuestaEstudianteRepositorio,
    ):
        self._perfil_repositorio = perfil_repositorio
        self._respuesta_repositorio = respuesta_repositorio

    def obtener_o_crear_perfil(self, estudiante_id: int) -> PerfilAcademico:
        perfil = self._perfil_repositorio.buscar_por_estudiante(estudiante_id)
        if perfil is None:
            perfil = PerfilAcademico(estudiante_id=estudiante_id, promedio_general=0.0)
            perfil = self._perfil_repositorio.guardar(perfil)
        return perfil

    def registrar_resultado_examen(self, estudiante_id: int, examen_id: int, nota_final: float) -> PerfilAcademico:
        """Caso de uso: 'Actualizar seguimiento academico tras un examen'."""
        perfil = self.obtener_o_crear_perfil(estudiante_id)

        evolucion = EvolucionNota(perfil_id=perfil.id, examen_id=examen_id, nota_final=nota_final)
        db.session.add(evolucion)

        notas = [e.nota_final for e in perfil.evoluciones_nota] + [nota_final]
        perfil.promedio_general = sum(notas) / len(notas)

        db.session.commit()
        return perfil

    def listar_perfiles(self) -> List[PerfilAcademico]:
        return self._perfil_repositorio.listar()
