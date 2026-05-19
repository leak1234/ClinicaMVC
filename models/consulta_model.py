from database import db
from datetime import datetime


class Consulta(db.Model):
    __tablename__ = 'consultas'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date,    nullable=False, default=datetime.utcnow)
    diagnostico = db.Column(db.Text,    nullable=False)
    tratamiento = db.Column(db.Text,    nullable=False)
    id_medico   = db.Column(db.Integer, db.ForeignKey('medicos.id'),   nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)

    # especificar las relaciones
    medico   = db.relationship('Medico',   back_populates='consultas')
    paciente = db.relationship('Paciente', back_populates='consultas')

    def __init__(self, fecha, diagnostico, tratamiento, id_medico, id_paciente):
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        self.fecha       = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.id_medico   = id_medico
        self.id_paciente = id_paciente

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Consulta.query.order_by(Consulta.fecha.desc()).all()

    @staticmethod
    def get_by_id(id):
        return Consulta.query.get_or_404(id)

    @staticmethod
    def get_by_paciente(id_paciente):
        return Consulta.query.filter_by(id_paciente=id_paciente)\
            .order_by(Consulta.fecha.desc()).all()

    @staticmethod
    def get_by_fecha(fecha_inicio, fecha_fin):
        return Consulta.query.filter(
            Consulta.fecha >= fecha_inicio,
            Consulta.fecha <= fecha_fin
        ).order_by(Consulta.fecha.desc()).all()

    def update(self, fecha=None, diagnostico=None, tratamiento=None,
               id_medico=None, id_paciente=None):
        if fecha:
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            self.fecha       = fecha
        if diagnostico:
            self.diagnostico = diagnostico
        if tratamiento:
            self.tratamiento = tratamiento
        if id_medico:
            self.id_medico   = id_medico
        if id_paciente:
            self.id_paciente = id_paciente
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
