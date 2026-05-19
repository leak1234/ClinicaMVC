from flask import request, redirect, url_for, Blueprint, flash, Response
from datetime import datetime
import csv
import io

from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consultas')


@consulta_bp.route('/')
def index():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin    = request.args.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        fi        = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        ff        = datetime.strptime(fecha_fin,    '%Y-%m-%d').date()
        consultas = Consulta.get_by_fecha(fi, ff)
    else:
        consultas = Consulta.get_all()

    return consulta_view.list(consultas, fecha_inicio, fecha_fin)


@consulta_bp.route('/create', methods=['GET', 'POST'])
def create():
    medicos   = Medico.get_all()
    pacientes = Paciente.get_all()

    if request.method == 'POST':
        fecha       = request.form['fecha']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_medico   = request.form['id_medico']
        id_paciente = request.form['id_paciente']

        consulta = Consulta(fecha, diagnostico, tratamiento,
                            int(id_medico), int(id_paciente))
        consulta.save()
        flash('Consulta registrada exitosamente.', 'success')
        return redirect(url_for('consulta.index'))

    return consulta_view.create(medicos, pacientes)


@consulta_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    consulta  = Consulta.get_by_id(id)
    medicos   = Medico.get_all()
    pacientes = Paciente.get_all()

    if request.method == 'POST':
        fecha       = request.form['fecha']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_medico   = request.form['id_medico']
        id_paciente = request.form['id_paciente']

        consulta.update(fecha=fecha, diagnostico=diagnostico,
                        tratamiento=tratamiento, id_medico=int(id_medico),
                        id_paciente=int(id_paciente))
        flash('Consulta actualizada exitosamente.', 'success')
        return redirect(url_for('consulta.index'))

    return consulta_view.edit(consulta, medicos, pacientes)


@consulta_bp.route('/delete/<int:id>')
def delete(id):
    consulta = Consulta.get_by_id(id)
    consulta.delete()
    flash('Consulta eliminada.', 'success')
    return redirect(url_for('consulta.index'))


@consulta_bp.route('/exportar')
def exportar():
    # extra: exportación de reporte CSV
    consultas = Consulta.get_all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Fecha', 'Paciente', 'Médico', 'Especialidad',
                     'Diagnóstico', 'Tratamiento'])

    for c in consultas:
        writer.writerow([
            c.id,
            c.fecha.strftime('%Y-%m-%d'),
            c.paciente.nombre,
            c.medico.nombre,
            c.medico.especialidad,
            c.diagnostico,
            c.tratamiento,
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=reporte_consultas.csv'}
    )
