"""Excepciones de dominio del subdominio Autenticacion_y_Usuarios.

Estilo de programacion: Error/Exception Handling. Cada regla de negocio
violada tiene su propia clase, en vez de propagar un `ValueError` generico
con un mensaje suelto o -peor- devolver `None`/codigos y obligar al
llamador a adivinar que salio mal. Heredan de `ValueError` a proposito:
el codigo cliente que ya hace `except ValueError` (controllers, tests)
sigue funcionando sin cambios, pero el codigo nuevo puede capturar el
tipo especifico (`except UsernameEnUsoError`) cuando le interese.
"""


class UsuarioError(ValueError):
    """Raiz de las excepciones de negocio del subdominio de usuarios."""


class UsernameEnUsoError(UsuarioError):
    def __init__(self, username: str):
        super().__init__(f"El username '{username}' ya esta en uso")
        self.username = username


class UsuarioNoEncontradoError(UsuarioError):
    def __init__(self, usuario_id: int):
        super().__init__(f"No existe un usuario con id {usuario_id}")
        self.id = usuario_id


class PasswordInvalidoError(UsuarioError):
    def __init__(self, motivo: str):
        super().__init__(f"Password invalido: {motivo}")
        self.motivo = motivo
