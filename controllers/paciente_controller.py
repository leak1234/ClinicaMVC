from flask import request, redirect, url_for, Blueprint, flash

from models.paciente_model import Paciente
from models.consulta_model import Consulta
from views import paciente_view

paciente_bp = Blueprint('paciente', __name__, url_prefix='/pacientes')


@paciente_bp.route('/')
def index():
    pacientes = Paciente.get_all()
    return paciente_view.list(pacientes)


@paciente_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre    = request.form['nombre']
        edad      = request.form['edad']
        direccion = request.form['direccion']
        telefono  = request.form['telefono']

        paciente = Paciente(nombre, int(edad), direccion, telefono)
        paciente.save()
        flash('Paciente registrado exitosamente.', 'success')
        return redirect(url_for('paciente.index'))

    return paciente_view.create()


@paciente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    paciente = Paciente.get_by_id(id)

    if request.method == 'POST':
        nombre    = request.form['nombre']
        edad      = request.form['edad']
        direccion = request.form['direccion']
        telefono  = request.form['telefono']

        paciente.update(nombre=nombre, edad=int(edad),
                        direccion=direccion, telefono=telefono)
        flash('Paciente actualizado exitosamente.', 'success')
        return redirect(url_for('paciente.index'))

    return paciente_view.edit(paciente)


@paciente_bp.route('/delete/<int:id>')
def delete(id):
    paciente = Paciente.get_by_id(id)
    paciente.delete()
    flash('Paciente eliminado.', 'success')
    return redirect(url_for('paciente.index'))


@paciente_bp.route('/historial/<int:id>')
def historial(id):
    # historial médico del paciente (extra)
    paciente  = Paciente.get_by_id(id)
    consultas = Consulta.get_by_paciente(id)
    return paciente_view.historial(paciente, consultas)
