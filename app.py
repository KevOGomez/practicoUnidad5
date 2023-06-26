from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db, Preceptor, Padre, Estudiante, Curso, Asistencia

db.init_app(app)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        clave = request.form['password']
        rol = request.form['rol']

        if rol == '0':
            hash = hashlib.md5(bytes(clave, encoding='utf-8'))
            user = Preceptor.query.filter_by(correo=correo, clave=hash.hexdigest()).first()
            if user != None:
                session['username'] = user.nombre
                session['email'] = user.correo
                session['id'] = user.id
                flash(f'Bienvenida {user.nombre}! \n Iniciaste como preceptor', 'correcto')
                return render_template('preceptor.html')
            else:
                flash('Correo, contraseña o rol incorrectos.', 'error')
                return render_template('login.html')
        elif rol == '1':
                print ('padre')
                user = Padre.query.filter_by(correo=correo, clave=clave).first()
                if user:
                    print ('user padre')
                    # Autenticación exitosa
                    return redirect
        flash('Correo, contraseña o rol incorrectos.', 'error')
    else:
        print('paso por aqui')
        return render_template('login.html')
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Aquí puedes realizar la lógica para obtener los datos necesarios para el dashboard
    # y luego renderizar el template del dashboard con esos datos
    return render_template('dashboard.html')

# Importante: reemplaza las rutas de los templates según corresponda

# FUNCIONALIDAD 2: Registrar asistencia de un curso

@app.route('/registrar_asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    estudiantes = []  # Definir como lista vacía por defecto
    
    if request.method == 'POST':
        id_clase = request.form['claseSelect']
        fecha_str = request.form['fechaInput']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        # Obtener estudiantes del curso seleccionado
        curso_seleccionado = Curso.query.filter_by(id=id_clase).first()
        estudiantes = curso_seleccionado.estudiantes
        
        for est, just in zip(request.form.getlist('estudiante_id'), request.form.getlist('justificacion')):
            asistencia = Asistencia()
            asistencia.fecha = fecha
            asistencia.codigoclase = id_clase
            asistencia.asistio = request.form['estudianteSelect']
            asistencia.justificacion = just
            asistencia.idestudiante = est
            asistencia.idpreceptor = session['id']  # Asociamos la asistencia al preceptor actual
            db.session.add(asistencia)
        
        db.session.commit()  # Movemos la operación de commit fuera del bucle
        
        flash('Asistencia guardada exitosamente.', 'correcto')
        return redirect(url_for('dashboard'))
    else:
        cursos = Curso.query.filter_by(idpreceptor=session['id']).all()
        divisiones = {}
        
        for curso in cursos:
            divisiones[curso.id] = curso.division
        
        return render_template('registrar_asistencia.html', cursos=cursos, estudiantes=estudiantes, divisiones=divisiones, usuario=session['id'])


# FUNCIONALIDAD 3: Obtener informe detallado

@app.route('/informe_detalles', methods=['GET', 'POST'])
def informe_detalles():
    if request.method == 'POST':
        course_id = request.form['course']
        
        students = Estudiante.query.filter_by(idcurso=course_id).order_by(Estudiante.nombre).all()
        
        details = []
        total_absences = 0
        
        for student in students:
            class1_present = Asistencia.query.filter_by(idestudiante=student.id, codigo_clase=1, asistio='s').count()
            class2_present = Asistencia.query.filter_by(idestudiante=student.id, codigo_clase=2, asistio='s').count()
            class1_absent_j = Asistencia.query.filter_by(idestudiante=student.id, codigo_clase=1, asistio='n',
                                                         justificacion='justificada').count()
            class1_absent_i = Asistencia.query.filter_by(idestudiante=student.id, codigo_clase=1, asistio='n',
                                                         justificacion='injustificada').count()
            class2_absent_j = Asistencia.query.filter_by(idestudiante=student.id, codigo_clase=2, asistio='n',
                                                         justificacion='justificada').count()
            class2_absent_i = Asistencia.query.filter_by(idestudiante=student.id, codigo_clase=2, asistio='n',
                                                         justificacion='injustificada').count()
            total_absences += class1_absent_i + class2_absent_i
            
            detail = {
                'student': student,
                'class1_present': class1_present,
                'class2_present': class2_present,
                'class1_absent_j': class1_absent_j,
                'class1_absent_i': class1_absent_i,
                'class2_absent_j': class2_absent_j,
                'class2_absent_i': class2_absent_i,
            }
            details.append(detail)
        
        return render_template('informar_detalles_resultado.html', details=details, total_absences=total_absences)
    
    courses = Curso.query.filter_by(idpreceptor=session['id']).all()
    return render_template('informar_detalles.html', courses=courses)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.debug = True
    app.run()