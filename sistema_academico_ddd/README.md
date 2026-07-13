# Sistema Académico

Este repositorio contiene la estructura inicial de mi proyecto de Sistema Académico, organizado siguiendo una arquitectura guiada por dominio (DDD).

## Propósito

Con este proyecto busco representar un sistema académico que permita gestionar usuarios, exámenes, respuestas de estudiantes, calificaciones automáticas, seguimiento académico, rankings y reportes institucionales.

La idea principal es separar bien las responsabilidades del sistema para que el código sea más ordenado, fácil de entender y sencillo de mantener.

## Funcionalidades principales

El sistema está pensado para cubrir las siguientes funcionalidades:

- Registro e inicio de sesión de usuarios.
- Gestión de roles: estudiante, docente, coordinador y director.
- Creación, configuración y asignación de exámenes.
- Envío de respuestas por parte de los estudiantes.
- Calificación automática de respuestas.
- Consulta de resultados y progreso académico.
- Generación de reportes institucionales.
- Consulta de rankings académicos.

## Modelo de dominio

He organizado el dominio en módulos para que cada parte del negocio tenga su propio espacio:

- **autenticacion_usuarios:** usuarios, credenciales y roles.
- **gestion_examenes:** exámenes, preguntas, configuración y asignaciones.
- **calificacion_automatica:** respuestas, calificaciones y servicio de calificación.
- **seguimiento_academico:** progreso, evolución de notas y desglose por área.
- **reportes_estadisticas:** reportes institucionales y estadísticas grupales.
- **rankings:** posiciones y mejores puntajes de estudiantes.
- **area_materia:** áreas y materias académicas.

## Puesta en marcha

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=run.py        # Windows (cmd): set FLASK_APP=run.py
flask db upgrade               # crea/actualiza el esquema via Alembic
python run.py                  # http://127.0.0.1:5000
```

Si modificas una entidad de dominio (nueva columna, nueva clase, etc.), genera una nueva migracion en vez de borrar la base de datos:

```bash
flask db migrate -m "Descripcion del cambio"
flask db upgrade
```

## Pruebas

```bash
pytest
```

## Stack tecnológico

| Capa                             | Tecnología                        |
|----------------------------------|-----------------------------------|
| Lenguaje                         | Python 3.11+                      |
| Framework Web MVC                | Flask 3                           |
| Framework ORM                    | SQLAlchemy (Flask-SQLAlchemy)     |
| Migraciones                      | Flask-Migrate (Alembic)           |
| Visión por computadora (OMR)     | OpenCV, NumPy, scikit-image       |
| Base de datos (dev)             | SQLite                            |

## Arquitectura (Domain-Driven Design en capas)

La organización de la arquitectura es la siguiente:



```
app/
├── presentacion/       # Controllers (Blueprints) + templates + static
├── aplicacion/          # Application Services (casos de uso)
├── dominio/             # Entidades, Value Objects, Domain Services,
│                        # Interfaces de Repositorio (por subdominio)
│   ├── autenticacion_usuarios/
│   ├── area_materia/
│   ├── gestion_examenes/
│   ├── calificacion_automatica/
│   ├── rankings/
│   ├── seguimiento_academico/
│   └── reportes_estadisticas/
└── infraestructura/
    ├── repositorios/            # Implementaciones concretas (SQLAlchemy)
    └── procesamiento_imagen/    # Servicio OMR (migrado del proyecto de escritorio)
```


