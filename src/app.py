import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Persona, Planeta, FavoritoPersona, FavoritoPlaneta

app = Flask(__name__)
app.url_map.strict_slashes = False

url_base_datos = os.getenv("DATABASE_URL")
if url_base_datos is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = url_base_datos.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRAR = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejar/serializar errores como un objeto JSON
@app.errorhandler(APIException)
def manejar_uso_invalido(error):
    return jsonify(error.a_dict()), error.codigo_estado

# Generar mapa de sitio con todos los endpoints
@app.route('/')
def mapa_sitio():
    return generate_sitemap(app)

@app.route('/usuario', methods=['GET'])
def manejar_bienvenida():
    respuesta = {
        "mensaje": "Hola, esta es tu respuesta GET /usuario"
    }
    return jsonify(respuesta), 200

# [GET] /usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_todos_usuarios():
    usuarios = Usuario.query.all()
    lista_usuarios = list(map(lambda usuario: usuario.a_dict(), usuarios))
    return jsonify(lista_usuarios), 200

# [GET] /usuarios/favoritos
@app.route('/usuarios/favoritos', methods=['GET'])
def obtener_favoritos_usuario():
    id_usuario = 1  # Reemplazar con el ID del usuario real cuando se implemente autenticación
    favoritos_personas = FavoritoPersona.query.filter_by(id_usuario=id_usuario).all()
    favoritos_planetas = FavoritoPlaneta.query.filter_by(id_usuario=id_usuario).all()
    lista_favoritos_personas = list(map(lambda fav: fav.a_dict(), favoritos_personas))
    lista_favoritos_planetas = list(map(lambda fav: fav.a_dict(), favoritos_planetas))
    return jsonify({
        "favoritos_personas": lista_favoritos_personas,
        "favoritos_planetas": lista_favoritos_planetas
    }), 200

# [POST] /favorito/planeta/<int:id_planeta>
@app.route('/favorito/planeta/<int:id_planeta>', methods=['POST'])
def agregar_favorito_planeta(id_planeta):
    id_usuario = 1  # Reemplazar con el ID del usuario real cuando se implemente autenticación
    favorito = FavoritoPlaneta(id_usuario=id_usuario, id_planeta=id_planeta)
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.a_dict()), 201

# [POST] /favorito/persona/<int:id_persona>
@app.route('/favorito/persona/<int:id_persona>', methods=['POST'])
def agregar_favorito_persona(id_persona):
    id_usuario = 1  # Reemplazar con el ID del usuario real cuando se implemente autenticación
    favorito = FavoritoPersona(id_usuario=id_usuario, id_persona=id_persona)
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.a_dict()), 201

# [DELETE] /favorito/planeta/<int:id_planeta>
@app.route('/favorito/planeta/<int:id_planeta>', methods=['DELETE'])
def eliminar_favorito_planeta(id_planeta):
    id_usuario = 1  # Reemplazar con el ID del usuario real cuando se implemente autenticación
    favorito = FavoritoPlaneta.query.filter_by(id_usuario=id_usuario, id_planeta=id_planeta).first()
    if favorito is None:
        raise APIException('Favorito no encontrado', codigo_estado=404)
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"mensaje": "Favorito planeta eliminado"}), 200

# [DELETE] /favorito/persona/<int:id_persona>
@app.route('/favorito/persona/<int:id_persona>', methods=['DELETE'])
def eliminar_favorito_persona(id_persona):
    id_usuario = 1  # Reemplazar con el ID del usuario real cuando se implemente autenticación
    favorito = FavoritoPersona.query.filter_by(id_usuario=id_usuario, id_persona=id_persona).first()
    if favorito is None:
        raise APIException('Favorito no encontrado', codigo_estado=404)
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"mensaje": "Favorito persona eliminado"}), 200

# [GET] /personas
@app.route('/personas', methods=['GET'])
def obtener_todas_personas():
    personas = Persona.query.all()
    lista_personas = list(map(lambda persona: persona.a_dict(), personas))
    return jsonify(lista_personas), 200

# [GET] /personas/<int:id_persona>
@app.route('/personas/<int:id_persona>', methods=['GET'])
def obtener_persona(id_persona):
    persona = Persona.query.get(id_persona)
    if persona is None:
        raise APIException('Persona no encontrada', codigo_estado=404)
    return jsonify(persona.a_dict()), 200

# [GET] /planetas
@app.route('/planetas', methods=['GET'])
def obtener_todos_planetas():
    planetas = Planeta.query.all()
    lista_planetas = list(map(lambda planeta: planeta.a_dict(), planetas))
    return jsonify(lista_planetas), 200

# [GET] /planetas/<int:id_planeta>
@app.route('/planetas/<int:id_planeta>', methods=['GET'])
def obtener_planeta(id_planeta):
    planeta = Planeta.query.get(id_planeta)
    if planeta is None:
        raise APIException('Planeta no encontrado', codigo_estado=404)
    return jsonify(planeta.a_dict()), 200

# Ejecutar solo si se ejecuta `$ python src/app.py`
if __name__ == '__main__':
    PUERTO = int(os.environ.get('PUERTO', 3000))
    app.run(host='0.0.0.0', port=PUERTO, debug=False)
