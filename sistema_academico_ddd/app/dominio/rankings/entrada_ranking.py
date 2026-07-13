"""Entidad de dominio EntradaRanking (posicion de un estudiante en el
ranking de un Examen)."""
from app.extensions import db


class EntradaRanking(db.Model):
    __tablename__ = "entradas_ranking"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    posicion = db.Column(db.Integer, nullable=False)
    nota_final = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"<EntradaRanking posicion={self.posicion} nota_final={self.nota_final}>"
