"""Capa de Dominio del Sistema Academico.

Organizada en modulos por subdominio (siguiendo el modelo de
arquitectura DDD en StarUML):
  - autenticacion_usuarios
  - area_materia
  - gestion_examenes
  - calificacion_automatica
  - rankings
  - seguimiento_academico
  - reportes_estadisticas

Cada modulo contiene sus Entidades/Value Objects (modelos SQLAlchemy),
sus Domain Services y su(s) interfaz(ces) de Repositorio (ABC), que
son implementadas concretamente en `app.infraestructura.repositorios`.
"""
