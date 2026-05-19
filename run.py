from flask import Flask, render_template, redirect, url_for, session, request

from database import db
from controllers.auth_controller    import auth_bp
from controllers.medico_controller  import medico_bp
from controllers.paciente_controller import paciente_bp
from controllers.consulta_controller import consulta_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']                     = 'clinica_secret_2026'

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(consulta_bp)


@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path.startswith(path) else ''
    return dict(is_active=is_active)


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('base.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
