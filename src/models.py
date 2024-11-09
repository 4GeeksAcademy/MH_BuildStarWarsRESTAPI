from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave_acceso = db.Column(db.String(80), unique=False, nullable=False)
    activo = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.correo

    def a_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "correo": self.correo
        }

class Persona(db.Model):
    __tablename__ = 'personas'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    url_info = db.Column(db.String(50), nullable=False)

    def a_dict(self):
        return {
            "id_persona": self.id_persona,
            "nombre": self.nombre,
            "altura": self.altura,
            "genero": self.genero,
            "fecha_creacion": self.fecha_creacion,
            "url_info": self.url_info
        }

class Planeta(db.Model):
    __tablename__ = 'planetas'
    id_planeta = db.Column(db.Integer, primary_key=True)
    nombre_planeta = db.Column(db.String(50), nullable=False)
    diametro_planeta = db.Column(db.Integer, nullable=False)
    clima_planeta = db.Column(db.String(50), nullable=False)
    poblacion_planeta = db.Column(db.String, nullable=False)
    url_info = db.Column(db.String(50), nullable=False)

    def a_dict(self):
        return {
            "id_planeta": self.id_planeta,
            "nombre_planeta": self.nombre_planeta,
            "diametro_planeta": self.diametro_planeta,
            "clima_planeta": self.clima_planeta,
            "poblacion_planeta": self.poblacion_planeta,
            "url_info": self.url_info
        }

class FavoritoPersona(db.Model):
    __tablename__ = 'favoritos_personas'
    id_favorito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id_persona'), nullable=False)
    usuario = db.relationship('Usuario', backref='favoritos_personas')
    persona = db.relationship('Persona', backref='favoritos_personas')

    def a_dict(self):
        return {
            "id_favorito": self.id_favorito,
            "id_usuario": self.id_usuario,
            "id_persona": self.id_persona
        }

class FavoritoPlaneta(db.Model):
    __tablename__ = 'favoritos_planetas'
    id_favorito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_planeta = db.Column(db.Integer, db.ForeignKey('planetas.id_planeta'), nullable=False)
    usuario = db.relationship('Usuario', backref='favoritos_planetas')
    planeta = db.relationship('Planeta', backref='favoritos_planetas')

    def a_dict(self):
        return {
            "id_favorito": self.id_favorito,
            "id_usuario": self.id_usuario,
            "id_planeta": self.id_planeta
        }
