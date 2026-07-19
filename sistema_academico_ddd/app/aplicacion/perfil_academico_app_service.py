"""Application Service: casos de uso de Seguimiento_Academico (consultar
y actualizar el perfil academico consolidado de un estudiante)."""
from typing import List

from app.extensions import db
from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico
from app.dominio.seguimiento_academico.perfil_academico_repositorio import (
    IPerfilAcademicoRepositorio,
)
from app.dominio.seguimiento_academico.evolucion_nota import EvolucionNota
from app.dominio.seguimiento_academico.excepciones import NotaInvalidaError
from app.dominio.seguimiento_academico.evolucion_academica import (
    EvolucionAcademicaEstado,
    EvolucionAcademicaLector,
    EvolucionAcademicaEscritor,
)
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 20.0


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

    def registrar_resultado_examen(
        self, estudiante_id: int, examen_id: int, nota_final: float
    ) -> PerfilAcademico:
        """Caso de uso: 'Actualizar seguimiento academico tras un examen'.

        Estilo Cookbook: se lee como una receta de pasos con nombre
        propio; el recalculo delega en el trio Trinity
        (Estado/Lector/Escritor) de `evolucion_academica.py`.

        ADVERTENCIA: el orden de los dos ultimos pasos importa. Hay que
        recalcular el promedio ANTES de registrar la evolucion nueva,
        porque el autoflush de SQLAlchemy adelantaria el INSERT al leer
        la relacion y la nota quedaria contada dos veces.
        """
        self._validar_nota(nota_final)
        perfil = self.obtener_o_crear_perfil(estudiante_id)
        self._recalcular_promedio_general(perfil, nota_final)
        self._registrar_evolucion(perfil, examen_id, nota_final)
        db.session.commit()
        return perfil

    def _validar_nota(self, nota_final: float) -> None:
        if not (NOTA_MINIMA <= nota_final <= NOTA_MAXIMA):
            raise NotaInvalidaError(nota_final)

    def _registrar_evolucion(
        self, perfil: PerfilAcademico, examen_id: int, nota_final: float
    ) -> None:
        evolucion = EvolucionNota(
            perfil_id=perfil.id, examen_id=examen_id, nota_final=nota_final
        )
        db.session.add(evolucion)

    def _recalcular_promedio_general(self, perfil: PerfilAcademico, nota_nueva: float) -> None:
        estado = EvolucionAcademicaEstado(perfil, nota_nueva)
        notas = EvolucionAcademicaLector.notas_historicas(estado)
        EvolucionAcademicaEscritor.aplicar_nuevo_promedio(estado, notas)

    def listar_perfiles(self) -> List[PerfilAcademico]:
        return self._perfil_repositorio.listar()
