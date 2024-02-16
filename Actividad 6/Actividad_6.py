import pytest
from auth import login, recuperar_contrasena, bloquear_cuenta

#objetos en la base de datos

class UsuarioSimulado:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class BaseDeDatosSimulada:
    usuarios = {}

    def crear_usuario(self, usuario):
        self.usuarios[usuario.username] = usuario

    def obtener_usuario_por_email(self, email):
        return self.usuarios.get(email)

#prueba

@pytest.mark.parametrize("username, password", [
    ("juan_perez", "123456"),
    ("maria_garcia", "contraseña"),
])
def test_login_valido(username, password):
    usuario = UsuarioSimulado(username, f"{username}@correo.com", password)
    base_de_datos = BaseDeDatosSimulada()
    base_de_datos.crear_usuario(usuario)

    assert login(username, password, base_de_datos)

def test_login_usuario_invalido():
    assert not login("usuarioinvalido", "123456", BaseDeDatosSimulada())

def test_login_contrasena_invalida():
    usuario = UsuarioSimulado("juan_perez", "juan.perez@correo.com", "123456")
    base_de_datos = BaseDeDatosSimulada()
    base_de_datos.crear_usuario(usuario)

    assert not login("juan_perez", "contraseñaincorrecta", base_de_datos)

def test_recuperar_contrasena(email):
    usuario = UsuarioSimulado("juan_perez", email, "123456")
    base_de_datos = BaseDeDatosSimulada()
    base_de_datos.crear_usuario(usuario)

    assert recuperar_contrasena(email, base_de_datos)

def test_bloquear_cuenta():
    base_de_datos = BaseDeDatosSimulada()
    for _ in range(6):
        login("usuarioinvalido", "contraseñaincorrecta", base_de_datos)

    assert bloquear_cuenta("usuarioinvalido", base_de_datos)
