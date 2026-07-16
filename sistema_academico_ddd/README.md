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

## Convenciones de Codificación: Práctica + Fragmento de Código

El proyecto sigue las convenciones de codificación de Python definidas en
[PEP 8](https://peps.python.org/pep-0008/), reforzadas con la extensión
**SonarLint** en el IDE para detectar bugs, code smells y vulnerabilidades.

**Convenciones aplicadas:**

- **Nombres**: `snake_case` para funciones y variables, `PascalCase` para
  clases (`ProcesadorDocumentos`, `DetectorDocumentosDual`), `UPPER_CASE`
  para constantes de módulo.
- **Idioma consistente**: todos los identificadores del dominio y la
  infraestructura están en español, evitando mezclar inglés/español en el
  mismo módulo.
- **Identificadores ASCII**: se evitan tildes y `ñ` en nombres de variables
  y parámetros (afecta la portabilidad y algunas herramientas de análisis
  estático).
- **Manejo de errores explícito**: se evita `except:` desnudo; se captura
  la excepción concreta esperada (o se registra con `logging` si debe
  capturarse `Exception` de forma amplia), nunca se descarta en silencio.
- **Sin números mágicos**: los umbrales y parámetros de negocio se extraen
  a constantes con nombre en la parte superior del módulo.
- **Sin rutas ni datos hardcodeados**: los scripts ejecutables (`if
  __name__ == "__main__":`) reciben la ruta de la imagen por argumento de
  línea de comandos en vez de una ruta fija de la máquina del autor.
- **Logging en vez de `print`**: los módulos de infraestructura registran
  errores con el módulo estándar `logging`, dejando `print` solo para la
  salida de los scripts de ejemplo.

**Fragmento de código — antes / después** (`app/infraestructura/procesamiento_imagen/corner_detector.py`):

```python
# Antes: except desnudo que oculta cualquier error
def limpiar_archivo_temporal():
    try:
        if os.path.exists(ruta_temporal_sombra):
            os.remove(ruta_temporal_sombra)
    except:
        pass

# Después: se captura la excepción esperada y se deja registro
def limpiar_archivo_temporal():
    try:
        if os.path.exists(ruta_temporal_sombra):
            os.remove(ruta_temporal_sombra)
    except OSError as error:
        logger.warning("No se pudo eliminar el archivo temporal %s: %s", ruta_temporal_sombra, error)
```

**Fragmento de código — números mágicos** (`app/infraestructura/procesamiento_imagen/document_scanner.py`):

```python
# Antes: umbrales sin nombre, dificil de entender o ajustar
if promedio <= 120:
    tipo = "muy_oscura"
elif promedio <= 140:
    tipo = "oscura"

# Después: constantes con nombre en la parte superior del modulo
UMBRAL_LUMINOSIDAD_MUY_OSCURA = 120
UMBRAL_LUMINOSIDAD_OSCURA = 140

if promedio <= UMBRAL_LUMINOSIDAD_MUY_OSCURA:
    tipo = "muy_oscura"
elif promedio <= UMBRAL_LUMINOSIDAD_OSCURA:
    tipo = "oscura"
```

**Fragmento de código — naming consistente** (`app/infraestructura/procesamiento_imagen/identificacion.py`):

```python
# Antes: nombres en ingles, inconsistentes con el resto del proyecto en espanol
def load_and_preprocess_image(image_path: str) -> np.ndarray: ...
def detect_filled_bubbles_in_dni(id_section: np.ndarray) -> List[int]: ...

# Después: nombres en espanol, consistentes con document_scanner.py y corner_detector.py
def cargar_y_preprocesar_imagen(ruta_imagen: str) -> np.ndarray: ...
def detectar_burbujas_llenas_dni(seccion_id: np.ndarray) -> List[int]: ...
```


