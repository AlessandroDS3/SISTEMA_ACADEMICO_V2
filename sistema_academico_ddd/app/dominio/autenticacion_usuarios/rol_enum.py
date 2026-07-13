"""Enumeracion de roles del sistema (UMLEnumeration RolEnum en el modelo)."""
import enum


class RolEnum(enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    DOCENTE = "DOCENTE"
    ESTUDIANTE = "ESTUDIANTE"
