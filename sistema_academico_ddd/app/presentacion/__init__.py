"""Capa de Presentacion del Sistema Academico.

Contiene los Controllers (Flask Blueprints), las plantillas Jinja2
(`templates/`) y los archivos estaticos (`static/`). Cada controller
delega toda la logica de negocio a su Application Service
correspondiente (capa `app.aplicacion`); no accede directamente al
dominio ni a SQLAlchemy salvo para consultas de lectura simples de
apoyo a la vista (p. ej. listar materias para un <select>).
"""
