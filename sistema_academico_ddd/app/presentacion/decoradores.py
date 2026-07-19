"""Decoradores reutilizables de la capa de presentacion.

Estilo de programacion: Error/Exception Handling. Sin este decorador,
cada accion POST de cada controller repetia el mismo
`try/except ValueError as error: flash(str(error))`. Centralizarlo en
un solo lugar evita que esa logica se copie y se desincronice entre
controllers.
"""
from functools import wraps


def manejar_errores_de_dominio(construir_redireccion):
    """`construir_redireccion(*args, **kwargs)` arma la respuesta a
    devolver si la vista decorada lanza un `ValueError` de dominio (o
    alguna de sus subclases, p.ej. `UsernameEnUsoError`)."""

    def decorador(vista):
        @wraps(vista)
        def envoltura(*args, **kwargs):
            from flask import flash

            try:
                return vista(*args, **kwargs)
            except ValueError as error:
                flash(str(error))
                return construir_redireccion(*args, **kwargs)

        return envoltura

    return decorador
