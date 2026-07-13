"""Pruebas de integracion de extremo a extremo usando el test client de
Flask: recorren las 3 capas (presentacion -> aplicacion -> infraestructura)
tal como lo haria un usuario real desde el navegador.
"""
from app.extensions import db as _db
from app.dominio.area_materia.area import Area
from app.dominio.area_materia.materia import Materia


def test_home_responde_200(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "Sistema Academico".encode() in respuesta.data or b"Bienvenido" in respuesta.data


def test_listar_usuarios_responde_200(client):
    assert client.get("/usuarios/").status_code == 200


def test_crear_editar_y_eliminar_usuario_por_http(client):
    # Crear
    respuesta = client.post(
        "/usuarios/nuevo",
        data={"username": "camila", "password": "clave123", "rol": "DOCENTE"},
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert b"camila" in respuesta.data

    # Editar (formulario)
    assert client.get("/usuarios/1/editar").status_code == 200

    respuesta = client.post(
        "/usuarios/1/editar",
        data={"username": "camila_editada", "rol": "ADMINISTRADOR"},
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert b"camila_editada" in respuesta.data
    assert b"camila_editada" in respuesta.data

    # Eliminar
    respuesta = client.post("/usuarios/1/eliminar", follow_redirects=True)
    assert respuesta.status_code == 200
    assert b"camila_editada" not in respuesta.data


def test_crear_username_duplicado_muestra_mensaje_de_error(client):
    client.post(
        "/usuarios/nuevo",
        data={"username": "camila", "password": "clave123", "rol": "DOCENTE"},
    )
    respuesta = client.post(
        "/usuarios/nuevo",
        data={"username": "camila", "password": "otra-clave", "rol": "ESTUDIANTE"},
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert "ya esta en uso".encode() in respuesta.data


def test_crear_editar_y_eliminar_examen_por_http(app, client):
    with app.app_context():
        area = Area(nombre="Ciencias de la Computacion")
        materia = Materia(nombre="Base de Datos II", codigo="BD2", area=area)
        _db.session.add_all([area, materia])
        _db.session.commit()
        materia_id = materia.id

    docente_resp = client.post(
        "/usuarios/nuevo",
        data={"username": "docente1", "password": "clave123", "rol": "DOCENTE"},
        follow_redirects=True,
    )
    assert docente_resp.status_code == 200

    # Crear examen
    respuesta = client.post(
        "/examenes/nuevo",
        data={
            "titulo": "Parcial 1",
            "materia_id": materia_id,
            "creado_por_id": 1,
            "numero_preguntas": 20,
            "numero_alternativas": 4,
            "puntaje_por_pregunta": 1.0,
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert b"Parcial 1" in respuesta.data

    # Editar examen
    assert client.get("/examenes/1/editar").status_code == 200

    respuesta = client.post(
        "/examenes/1/editar",
        data={
            "titulo": "Parcial 1 - Revisado",
            "materia_id": materia_id,
            "numero_preguntas": 25,
            "numero_alternativas": 5,
            "puntaje_por_pregunta": 2.0,
        },
        follow_redirects=True,
    )
    assert respuesta.status_code == 200
    assert b"Parcial 1 - Revisado" in respuesta.data

    # Eliminar examen
    respuesta = client.post("/examenes/1/eliminar", follow_redirects=True)
    assert respuesta.status_code == 200
    assert b"Parcial 1 - Revisado" not in respuesta.data
