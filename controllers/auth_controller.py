from flask import request, redirect, url_for, Blueprint, flash, session

from models.usuario_model import Usuario
from views import auth_view

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = Usuario.get_by_username(username)
        if usuario and usuario.verify_password(password):
            session['user_id']  = usuario.id
            session['username'] = usuario.username
            flash(f'Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('home'))

        flash('Credenciales incorrectas.', 'danger')

    return auth_view.login()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre   = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        confirm  = request.form['confirm']

        if password != confirm:
            flash('Las contraseñas no coinciden.', 'danger')
            return auth_view.register()

        if Usuario.get_by_username(username):
            flash('El nombre de usuario ya existe.', 'danger')
            return auth_view.register()

        usuario = Usuario(nombre, username, password, rol='admin')
        usuario.save()
        flash('Cuenta creada. Puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return auth_view.register()


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth.login'))
