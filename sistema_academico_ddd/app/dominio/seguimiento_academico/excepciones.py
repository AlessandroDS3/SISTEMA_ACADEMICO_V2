"""Excepciones de dominio del subdominio Seguimiento_Academico.

Estilo de programacion: Error/Exception Handling (ver tambien
`app.dominio.autenticacion_usuarios.excepciones`)."""


class SeguimientoAcademicoError(ValueError):
    """Raiz de las excepciones de negocio del subdominio de seguimiento
    academico."""


class NotaInvalidaError(SeguimientoAcademicoError):
    def __init__(self, nota_final: float):
        super().__init__(f"La nota final debe estar entre 0 y 20 (recibido: {nota_final})")
        self.nota_final = nota_final


class PerfilNoEncontradoError(SeguimientoAcademicoError):
    """Se lanza al operar sobre un perfil academico que no existe.

    Practica Clean Code (Tratamiento de Errores): se prefiere una
    excepcion con contexto antes que un codigo de error (`return False`),
    que obligaba a cada llamador a comprobar el valor devuelto y
    silenciaba la causa real del fallo.
    """

    def __init__(self, perfil_id: int):
        super().__init__(f"No existe un perfil academico con id {perfil_id}")
        self.perfil_id = perfil_id
