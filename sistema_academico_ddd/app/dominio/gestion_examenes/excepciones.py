"""Excepciones de dominio del subdominio Gestion_de_Examenes.

Estilo de programacion: Error/Exception Handling (misma idea que en
`app.dominio.autenticacion_usuarios.excepciones`, aplicada aqui)."""


class GestionExamenesError(ValueError):
    """Raiz de las excepciones de negocio del subdominio de examenes."""


class ExamenNoEncontradoError(GestionExamenesError):
    def __init__(self, id: int):
        super().__init__(f"No existe un examen con id {id}")
        self.id = id


class NumeroPreguntasInvalidoError(GestionExamenesError):
    def __init__(self, numero_preguntas: int):
        super().__init__(
            f"El numero de preguntas debe ser mayor a 0 (recibido: {numero_preguntas})"
        )
        self.numero_preguntas = numero_preguntas


class PreguntaDuplicadaError(GestionExamenesError):
    def __init__(self, numero_pregunta: int):
        super().__init__(
            f"Ya existe una pregunta numero {numero_pregunta} en el banco de este examen"
        )
        self.numero_pregunta = numero_pregunta
