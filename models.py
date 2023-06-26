""""Usuarios
Los usuarios de la aplicación son los preceptores y padres registrados.
Reglas de negocio globales
1. Un preceptor tiene asignado uno o más cursos.
2. Un curso tiene asignado solo un preceptor.
3. A un curso pertenecen muchos estudiantes.
4. Un estudiante pertenece solo a un curso.
5. Un padre es vinculado a uno o más estudiantes.
6. Un estudiante es vinculado a un padre.
7. Los tipos de clases están codificados, correspondiendo a la clase de aula el código 1 
y a la clase de educación física el código 2.
8. Una inasistencia a clase de aula se computa como una falta.
9. Una inasistencia a clase de educación física se computa como media falta.
10. En todas las páginas de la aplicación debe figurar el nombre del colegio. """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint

db = SQLAlchemy()

class Preceptor(db.Model):
    __tablename__= 'preceptor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)    
    clave = db.Column(db.String(120), nullable=False)
    curso = db.relationship('Curso', backref='preceptor', cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint('correo', name='uq_preceptor_correo'),
    )

class Curso(db.Model):
    __tablename__= 'curso'
    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False)
    division = db.Column(db.String(120), nullable=False)
    idpreceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id'))
    estudiante = db.relationship('Estudiante', backref='curso', cascade="all, delete-orphan")        

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    dni = db.Column(db.String(120), nullable=False, unique=True)
    idcurso = db.Column(db.Integer, db.ForeignKey('curso.id'))
    idpadre = db.Column(db.Integer, db.ForeignKey('padre.id'))
    asistencia = db.relationship('Asistencia', backref='estudiante', cascade="all, delete-orphan")

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(100))
    codigoclase = db.Column(db.Integer, nullable=False)
    asistio = db.Column(db.String(1), nullable=False)
    justificacion = db.Column(db.Text(200))
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))

class Padre(db.Model):
    __tablename__ = 'padre'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)
    estudiante = db.relationship('Estudiante', backref='padre', cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint('correo', name='uq_preceptor_correo'),
    )