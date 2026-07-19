"""Entidad de dominio Credencial (token de sesion asociado a un Usuario)."""
from datetime import timedelta
import secrets

from app.dominio.tiempo import ahora_utc
from app.extensions import db


class Credencial(db.Model):
    __tablename__ = "credenciales"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    token_sesion = db.Column(db.String(128), unique=True, nullable=False)
    expira_en = db.Column(db.DateTime, nullable=False)

    usuario = db.relationship("Usuario", back_populates="credenciales")

    @staticmethod
    def generar_para(usuario_id: int, horas_validez: int = 8) -> "Credencial":
        return Credencial(
            usuario_id=usuario_id,
            token_sesion=secrets.token_hex(32),
            expira_en=ahora_utc() + timedelta(hours=horas_validez),
        )

    def esta_vigente(self) -> bool:
        return ahora_utc() < self.expira_en
