"""API REST (JSON) del subdominio Autenticacion_y_Usuarios.

Convive con `usuario_controller.py` (que sirve las paginas HTML) sin
reemplazarlo: esta es una puerta de entrada adicional al mismo
`UsuarioAppService`, pensada para consumidores que hablan JSON en vez
de formularios HTML.

Estilos de programacion:
  - Restful: la URL identifica el RECURSO (`/api/usuarios`,
    `/api/usuarios/<id>`) y el METODO HTTP identifica la ACCION
    (GET=leer, POST=crear, PUT=actualizar, DELETE=eliminar), en vez de
    codificar el verbo en la propia URL como hacen las rutas HTML
    (`/usuarios/nuevo`, `/usuarios/<id>/editar`).
  - Things: `UsuarioAPI` (Flask `MethodView`) es un "Thing": un unico
    objeto que agrupa el estado del recurso "usuario" junto con todo
    el comportamiento sobre ese recurso (`get`/`post`/`put`/`delete`),
    en vez de 4 funciones sueltas sin relacion explicita entre si.
  - Cookbook: `post` y `put` se leen como una receta de pasos con
    nombre propio (leer datos del cuerpo -> ejecutar el caso de uso ->
    serializar la respuesta).
"""
from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app.contenedor import usuario_app_service
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.dominio.autenticacion_usuarios.excepciones import UsuarioError

api_usuario_bp = Blueprint("api_usuario", __name__)


def _serializar(usuario: Usuario) -> dict:
    return {"id": usuario.id, "username": usuario.username, "rol": usuario.rol.value}


class UsuarioAPI(MethodView):

    def get(self, usuario_id: int = None):
        servicio = usuario_app_service()
        if usuario_id is None:
            return jsonify([_serializar(u) for u in servicio.listar_usuarios()])
        usuario = servicio.obtener_por_id(usuario_id)
        if usuario is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(_serializar(usuario))

    def post(self):
        try:
            datos = self._leer_datos_creacion()
            usuario = self._ejecutar_registro(datos)
            return self._respuesta_creado(usuario)
        except UsuarioError as error:
            return jsonify({"error": str(error)}), 400

    def _leer_datos_creacion(self) -> dict:
        cuerpo = request.get_json(silent=True) or {}
        return {
            "username": cuerpo.get("username"),
            "password": cuerpo.get("password"),
            "rol": RolEnum(cuerpo.get("rol", RolEnum.ESTUDIANTE.value)),
        }

    def _ejecutar_registro(self, datos: dict) -> Usuario:
        return usuario_app_service().registrar_usuario(**datos)

    def _respuesta_creado(self, usuario: Usuario):
        return jsonify(_serializar(usuario)), 201

    def put(self, usuario_id: int):
        try:
            datos = self._leer_datos_actualizacion()
            usuario = usuario_app_service().actualizar_usuario(usuario_id, **datos)
            return jsonify(_serializar(usuario))
        except UsuarioError as error:
            return jsonify({"error": str(error)}), 400

    def _leer_datos_actualizacion(self) -> dict:
        cuerpo = request.get_json(silent=True) or {}
        return {
            "username": cuerpo.get("username"),
            "rol": RolEnum(cuerpo.get("rol", RolEnum.ESTUDIANTE.value)),
            "password": cuerpo.get("password") or None,
        }

    def delete(self, usuario_id: int):
        eliminado = usuario_app_service().eliminar_usuario(usuario_id)
        if not eliminado:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return "", 204


_usuario_api_view = UsuarioAPI.as_view("usuario_api")
api_usuario_bp.add_url_rule(
    "/", defaults={"usuario_id": None}, view_func=_usuario_api_view, methods=["GET"]
)
api_usuario_bp.add_url_rule("/", view_func=_usuario_api_view, methods=["POST"])
api_usuario_bp.add_url_rule(
    "/<int:usuario_id>", view_func=_usuario_api_view, methods=["GET", "PUT", "DELETE"]
)
