#!/usr/bin/python
# -*- coding: utf-8 -*-

from Dominio_Autenticacion_Usuarios.IUsuarioRepositorio import IUsuarioRepositorio


class UsuarioRepositorioImpl(IUsuarioRepositorio):
    def __init__(self):
        pass

    def guardar(self, usuario):
        pass

    def buscarPorId(self, id):
        pass

    def buscarPorUsername(self, username):
        pass

    def actualizar(self, usuario):
        pass

    def eliminar(self, id):
        pass
