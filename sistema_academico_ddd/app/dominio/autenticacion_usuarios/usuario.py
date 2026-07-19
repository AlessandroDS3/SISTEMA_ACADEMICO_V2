"""Entidad de dominio Usuario (raiz de agregado del subdominio
Autenticacion_y_Usuarios).
"""
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.dominio.autenticacion_usuarios.excepciones import PasswordInvalidoError


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(RolEnum), nullable=False, default=RolEnum.ESTUDIANTE)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    credenciales = db.relationship(
        "Credencial", back_populates="usuario", cascade="all, delete-orphan"
    )

    def establecer_password(self, password_plano: str) -> None:
        """Valida y aplica la contrasena. La entidad protege su propio
        invariante (Error/Exception Handling) en vez de confiar en que
        cada llamador la valide por su cuenta."""
        if len(password_plano) < 6:
            raise PasswordInvalidoError("debe tener al menos 6 caracteres")
        self.password_hash = generate_password_hash(password_plano)

    def verificar_password(self, password_plano: str) -> bool:
        return check_password_hash(self.password_hash, password_plano)

    def actualizar_perfil(self, username: str, rol: RolEnum) -> None:
        """Estilo Things: el propio Usuario sabe como mutar su estado
        (username/rol), en vez de que la capa de aplicacion le asigne
        los atributos directamente desde afuera (`usuario.rol = rol`)."""
        self.username = username
        self.rol = rol

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} username={self.username!r} rol={self.rol}>"
