# Tablero Kanban / Scrum — Sistema Academico

Tablero de gestion del proyecto basado en la plantilla **User Story Mapping**
en Trello, tal como pide la Practica 9.

> **Enlace al tablero:** _(pegar aqui la URL publica del tablero de Trello)_

El tablero combina dos vistas: el **mapa de historias por rol** (parte superior,
que agrupa las historias segun el actor que las ejecuta) y el **flujo Kanban/Scrum**
(parte inferior, con el Product Backlog, el Sprint Backlog y las etapas del flujo).

## 1. Mapa de historias por rol (User Story Mapping)

Cada columna es un actor del sistema; debajo estan sus requisitos funcionales (RF),
historias de funcionalidad (HF) e historias no funcionales (HNF).

### Coordinador Academico

| Codigo | Historia / Requisito |
|---|---|
| RF.6 | Gestion de usuarios |
| HF.6.1 | Iniciar sesion segun rol |
| HF.6.2 | Registrar docentes y estudiantes |
| RF.1 | Gestion de examenes |
| HF.1.1 | Crear examen desde banco |
| HF.1.2 | Programar fecha y hora |
| EF.1.3 | Gestionar examenes |
| HF.1.3.1 | Asignar a grupo de estudiantes |
| HF.1.3.2 | Revisar clave de respuestas |
| HF.1.3.m | Configurar puntaje por pregunta |
| RF.5 | Banco de preguntas |
| HF.5.1 | Agregar pregunta al banco |
| HF.5.2 | Editar / eliminar preguntas |
| RF.2 | Calificacion automatica |
| HF.2.2 | Revisar y ajustar clave antes de corregir |
| HF.2.n | Recalificar si se corrige la clave |
| RF.3 | Gestion de rankings |
| HF.3.2 | Filtrar ranking por curso / periodo |
| RF.4 | Seguimiento academico |
| F.4.n | Estadisticas grupales por seccion |

### Estudiante

| Codigo | Historia / Requisito |
|---|---|
| RF.3 | Gestion de rankings |
| HF.3.1 | Ver posicion en ranking general |
| HF.6.1 | Iniciar sesion segun mi rol |
| RF.6 | Gestion de usuarios |
| RF.4 | Seguimiento academico |
| EF.4.1 | Visualizar progreso academico propio |

### Director

| Codigo | Historia / Requisito |
|---|---|
| RF.7 | Reportes y estadisticas |
| HF.7.1 | Descargar reporte general por periodo |
| HF.7.n | Exportar estadisticas por seccion |

### Sistema (requisitos no funcionales)

| Codigo | Historia / Requisito |
|---|---|
| RNF.1 | Seguridad |
| HNF.1.1 | Cifrar contrasenas y datos de examenes |
| RNF.2 | Rendimiento |
| HNF.2.1 | Responder operaciones en < 3 segundos |
| RNF.3 | Usabilidad |

## 2. Flujo Kanban / Scrum

### Product Backlog (orden de prioridad)

1. RF.6 -> RF.1 -> RF.2
2. RF.3 -> RF.4 -> RNF.1
3. RF.5 -> RF.7 -> RNF.2

### Sprint Backlog (iteracion actual)

| Historia | Checklist | Responsable(s) | Plazo |
|---|---|---|---|
| HF.6.1 — Iniciar sesion con credenciales segun rol | 13/13 | DS, SC | 21 jul |
| HF.6.2 — Registrar nuevos docentes y estudiantes | 0/12 | CC | — |
| HF.1.1 — Crear examen seleccionando preguntas del banco | 0/13 | SC | — |
| HF.1.2 — Programar fecha y hora del examen | — | — | — |
| HF.1.3 — Asignar examen a grupo de estudiantes | — | — | — |
| ACT.7 — Disenar arquitectura en capas del sistema | — | — | — |

### Etapas del flujo

`Product Backlog` -> `Sprint Backlog` -> `Kanban (En progreso)` -> `Hecho`

## 3. Relacion con el codigo del repositorio

Cada requisito funcional del tablero se corresponde con un subdominio del modelo
DDD implementado en `sistema_academico_ddd/app/dominio/`:

| Requisito (Trello) | Subdominio / modulo implementado |
|---|---|
| RF.6 Gestion de usuarios | `autenticacion_usuarios` |
| RF.1 Gestion de examenes / RF.5 Banco de preguntas | `gestion_examenes` |
| RF.2 Calificacion automatica | `calificacion_automatica` + `infraestructura/procesamiento_imagen` |
| RF.3 Gestion de rankings | `rankings` |
| RF.4 Seguimiento academico | `seguimiento_academico` |
| RF.7 Reportes y estadisticas | `reportes_estadisticas` |
| Areas y materias (soporte) | `area_materia` |

> **Evidencia pendiente:** adjuntar una captura de pantalla del tablero real de
> Trello en `docs/trello/` (por ejemplo `captura_tablero.png`) antes de la entrega.
