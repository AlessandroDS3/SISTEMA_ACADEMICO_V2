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
