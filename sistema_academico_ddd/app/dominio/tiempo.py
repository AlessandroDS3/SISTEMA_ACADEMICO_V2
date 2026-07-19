"""Utilidad de tiempo compartida por las entidades del dominio."""
from datetime import datetime, timezone


def ahora_utc() -> datetime:
    """Fecha y hora actual en UTC, sin zona horaria (naive).

    Reemplaza a ``datetime.utcnow()`` (deprecado desde Python 3.12) sin
    cambiar el tipo almacenado: las columnas ``DateTime`` del proyecto
    guardan valores naive en UTC, por lo que se descarta el ``tzinfo``
    para que las comparaciones con datos ya persistidos sigan siendo
    validas.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
