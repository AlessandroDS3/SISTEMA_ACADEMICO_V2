"""Pruebas de integracion de los estilos agregados en Lab 10 sobre la
capa de presentacion: Restful + Things (UsuarioAPI, un MethodView) y
Cookbook (post/put leidos como receta de pasos)."""


def test_get_lista_usuarios_vacia_responde_200_con_lista_json(client):
    respuesta = client.get("/api/usuarios/")
    assert respuesta.status_code == 200
    assert respuesta.get_json() == []


def test_post_crea_usuario_y_responde_201_con_el_recurso(client):
    respuesta = client.post(
        "/api/usuarios/",
        json={"username": "camila", "password": "clave123", "rol": "DOCENTE"},
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.get_json()
    assert cuerpo["username"] == "camila"
    assert cuerpo["rol"] == "DOCENTE"
    assert "id" in cuerpo


def test_post_con_username_duplicado_responde_400_con_error_de_dominio(client):
    client.post(
        "/api/usuarios/",
        json={"username": "camila", "password": "clave123", "rol": "DOCENTE"},
    )
    respuesta = client.post(
        "/api/usuarios/",
        json={"username": "camila", "password": "otra-clave", "rol": "ESTUDIANTE"},
    )
    assert respuesta.status_code == 400
    assert "ya esta en uso" in respuesta.get_json()["error"]


def test_put_actualiza_usuario_existente(client):
    creado = client.post(
        "/api/usuarios/",
        json={"username": "camila", "password": "clave123", "rol": "ESTUDIANTE"},
    ).get_json()

    respuesta = client.put(
        f"/api/usuarios/{creado['id']}", json={"username": "camila_docente", "rol": "DOCENTE"}
    )

    assert respuesta.status_code == 200
    assert respuesta.get_json()["username"] == "camila_docente"


def test_delete_elimina_usuario_existente(client):
    creado = client.post(
        "/api/usuarios/",
        json={"username": "camila", "password": "clave123", "rol": "ESTUDIANTE"},
    ).get_json()

    respuesta = client.delete(f"/api/usuarios/{creado['id']}")

    assert respuesta.status_code == 204
    assert client.get(f"/api/usuarios/{creado['id']}").status_code == 404
