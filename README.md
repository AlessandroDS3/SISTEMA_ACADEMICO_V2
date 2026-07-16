# Sistema Academico

Este repositorio contiene la estructura inicial de mi proyecto de Sistema Academico, organizado siguiendo una arquitectura guiada por dominio (DDD).

## Proposito

Con este proyecto busco representar un sistema academico que permita gestionar usuarios, examenes, respuestas de estudiantes, calificaciones automaticas, seguimiento academico, rankings y reportes institucionales.

La idea principal es separar bien las responsabilidades del sistema para que el codigo sea mas ordenado, facil de entender y sencillo de mantener.

## Funcionalidades principales

El sistema esta pensado para cubrir estas funcionalidades:

- Registro e inicio de sesion de usuarios.
- Gestion de roles: estudiante, docente, coordinador y director.
- Creacion, configuracion y asignacion de examenes.
- Envio de respuestas por parte de los estudiantes.
- Calificacion automatica de respuestas.
- Consulta de resultados y progreso academico.
- Generacion de reportes institucionales.
- Consulta de rankings academicos.

## Modelo de dominio

Organice el dominio en modulos para que cada parte del negocio tenga su propio espacio:

- `autenticacion_usuarios`: usuarios, credenciales y roles.
- `gestion_examenes`: examenes, preguntas, configuracion y asignaciones.
- `calificacion_automatica`: respuestas, calificaciones y servicio de calificacion.
- `seguimiento_academico`: progreso, evolucion de notas y desglose por area.
- `reportes_estadisticas`: reportes institucionales y estadisticas grupales.
- `rankings`: posiciones y mejores puntajes de estudiantes.
- `area_materia`: areas y materias academicas.

## Arquitectura

Organice el repositorio en cuatro capas principales:

- `presentacion`: contiene los controladores del sistema.
- `aplicacion`: contiene los servicios de aplicacion y casos de uso.
- `dominio`: contiene las entidades, value objects, servicios de dominio, factories e interfaces de repositorio.
- `infraestructura`: contiene las implementaciones concretas de los repositorios.

## Estructura del proyecto

```txt
SISTEMA_ACADEMICO_V2/
├── docs/
│   └── uml/
│       └── ISUML.mdj
└── sistema_academico_ddd/     # Implementacion (Python/Flask), ver su propio README
    ├── app/
    │   ├── presentacion/
    │   ├── aplicacion/
    │   ├── dominio/
    │   └── infraestructura/
    ├── migrations/
    └── tests/
```

## Diagramas UML

El diagrama original del proyecto se encuentra en:

```txt
docs/uml/ISUML.mdj
```

Alli se encuentra el modelo UML con los casos de uso, clases, paquetes y la vista general de arquitectura.

## Estado del proyecto

La implementacion del sistema (Python, Flask, SQLAlchemy) ya esta en curso dentro
de [`sistema_academico_ddd/`](sistema_academico_ddd/README.md), que incluye la
arquitectura DDD en capas, las convenciones de codificacion aplicadas y las
instrucciones de puesta en marcha y pruebas.
