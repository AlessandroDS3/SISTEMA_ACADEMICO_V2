"""Excepciones de dominio del subdominio Area_y_Materia.

Estilo de programacion: Error/Exception Handling (ver tambien
`app.dominio.autenticacion_usuarios.excepciones` para la misma idea
aplicada al subdominio de usuarios).
"""


class AreaMateriaError(ValueError):
    """Raiz de las excepciones de negocio del subdominio Area_y_Materia."""


class MateriaDuplicadaError(AreaMateriaError):
    def __init__(self, codigo: str):
        super().__init__(f"La materia con codigo '{codigo}' ya existe en esta area")
        self.codigo = codigo
